"""Link-integrity check: find markdown links `[text](target.md)` whose target
file is missing in a flat vault corpus.

Scans an already-generated vault (no regeneration). Target resolution is
file-level (`Some_Page.md` exists in the output directory).
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# `[text](file.md)` or `[text](file.md#anchor)`; capture target (group 1) and
# optional anchor (group 2). Link text may contain escaped brackets.
_MD_LINK_RE = re.compile(
    r"(?<!\\)\[((?:[^\[\]\\]|\\.)*?)\]\(([^)#]+\.md)(?:#([\w.\-]+))?\)"
)

# Generated bookkeeping files — scan neither as sources nor as targets.
_SKIP_STEMS = {
    "_meta",
    "_errors",
    "_unresolved",
    "_ungrounded",
    "_dangling",
    "_truncated",
    "_collisions",
}


def _strip_code_fences(text: str) -> str:
    """Drop fenced code blocks (```…```)."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def _headings(text: str) -> set[str]:
    """Casefolded `#` / `##` heading texts of a (fence-stripped) md document."""
    out: set[str] = set()
    for line in text.splitlines():
        if line.startswith("## "):
            out.add(line[3:].strip().casefold())
        elif line.startswith("# "):
            out.add(line[2:].strip().casefold())
    return out


def _target_name(href_target: str) -> str:
    """Normalize link target to a bare filename (flat vault)."""
    return Path(href_target.strip().replace("\\", "/")).name


@dataclass
class LinkReport:
    md_files: int = 0
    total_links: int = 0
    unique_targets: int = 0
    dangling_targets: int = 0
    dangling_occurrences: int = 0
    # dangling target filename → (occurrences, first source file name)
    dangling: dict[str, tuple[int, str]] = field(default_factory=dict)
    # first path segment before `__` or `.` → dangling occurrences
    by_prefix: dict[str, int] = field(default_factory=dict)
    anchor_links: int = 0
    ungrounded_anchors: int = 0
    ungrounded_occurrences: int = 0
    # "file.md#anchor" → (occurrences, first source file name)
    ungrounded: dict[str, tuple[int, str]] = field(default_factory=dict)


def check_links(out_dir: Path) -> LinkReport:
    existing: set[str] = set()
    headings: dict[str, set[str]] = {}
    md_files: list[Path] = []
    refs: list[tuple[str, str | None, str]] = []

    for p in sorted(out_dir.glob("*.md")):
        if p.stem in _SKIP_STEMS:
            continue
        existing.add(p.name)
        md_files.append(p)
        text = _strip_code_fences(p.read_text(encoding="utf-8"))
        headings[p.name] = _headings(text)
        for m in _MD_LINK_RE.finditer(text):
            target = _target_name(m.group(2))
            if not target:
                continue
            anchor = m.group(3)
            refs.append((target, anchor, p.name))

    targets_seen: set[str] = set()
    dangling_count: dict[str, int] = defaultdict(int)
    dangling_first: dict[str, str] = {}
    ungrounded_count: dict[str, int] = defaultdict(int)
    ungrounded_first: dict[str, str] = {}
    total_links = 0
    anchor_links = 0

    for target, anchor, src in refs:
        total_links += 1
        targets_seen.add(target)
        if target not in existing:
            dangling_count[target] += 1
            dangling_first.setdefault(target, src)
            continue
        if anchor is None:
            continue
        anchor_links += 1
        if anchor.casefold() not in headings.get(target, ()):
            key = f"{target}#{anchor}"
            ungrounded_count[key] += 1
            ungrounded_first.setdefault(key, src)

    by_prefix: dict[str, int] = defaultdict(int)
    dangling: dict[str, tuple[int, str]] = {}
    occurrences = 0
    for target, cnt in dangling_count.items():
        dangling[target] = (cnt, dangling_first[target])
        occurrences += cnt
        stem = target[:-3] if target.endswith(".md") else target
        prefix = stem.split("__", 1)[0].split(".", 1)[0]
        by_prefix[prefix] += cnt

    ungrounded: dict[str, tuple[int, str]] = {}
    ung_occ = 0
    for key, cnt in ungrounded_count.items():
        ungrounded[key] = (cnt, ungrounded_first[key])
        ung_occ += cnt

    return LinkReport(
        md_files=len(md_files),
        total_links=total_links,
        unique_targets=len(targets_seen),
        dangling_targets=len(dangling_count),
        dangling_occurrences=occurrences,
        dangling=dangling,
        by_prefix=dict(by_prefix),
        anchor_links=anchor_links,
        ungrounded_anchors=len(ungrounded_count),
        ungrounded_occurrences=ung_occ,
        ungrounded=ungrounded,
    )


def write_dangling_log(out_dir: Path, report: LinkReport) -> None:
    """Write _dangling.log (target<TAB>occurrences<TAB>sample-source), or remove
    it when there are no dangling links."""
    log_path = out_dir / "_dangling.log"
    if not report.dangling:
        if log_path.exists():
            log_path.unlink()
        return
    lines = [
        f"{target}\t{cnt}\t{src}"
        for target, (cnt, src) in sorted(
            report.dangling.items(), key=lambda kv: (-kv[1][0], kv[0])
        )
    ]
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ungrounded_log(out_dir: Path, report: LinkReport) -> None:
    """Write _ungrounded.log (file.md#anchor<TAB>occurrences<TAB>sample-source),
    or remove it when every anchor is grounded."""
    log_path = out_dir / "_ungrounded.log"
    if not report.ungrounded:
        if log_path.exists():
            log_path.unlink()
        return
    lines = [
        f"{key}\t{cnt}\t{src}"
        for key, (cnt, src) in sorted(
            report.ungrounded.items(), key=lambda kv: (-kv[1][0], kv[0])
        )
    ]
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@dataclass
class RemediateReport:
    files_changed: int = 0
    links_remediated: int = 0
    links_stripped: int = 0


def _unescape_link_text(text: str) -> str:
    return text.replace(r"\[", "[").replace(r"\]", "]").replace(r"\\", "\\")


def _remediate_fence_stripped(text: str, existing: set[str], alias: dict[str, str] | None) -> tuple[str, int, int]:
    """Remediate links outside code fences. Returns (new_text, remediated, stripped)."""
    remediated = 0
    stripped = 0
    out: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        def repl(m: re.Match[str]) -> str:
            nonlocal remediated, stripped
            label = m.group(1)
            target = _target_name(m.group(2))
            anchor = m.group(3)
            resolved = (alias or {}).get(target, target)
            if resolved in existing:
                if resolved != target:
                    remediated += 1
                href = resolved + (f"#{anchor}" if anchor else "")
                return f"[{label}]({href})"
            stripped += 1
            return _unescape_link_text(label)

        out.append(_MD_LINK_RE.sub(repl, line))
    return "".join(out), remediated, stripped


def remediate_vault_links(
    out_dir: Path,
    alias: dict[str, str] | None = None,
    skip_stems: set[str] | None = None,
) -> RemediateReport:
    """Переписать известные алиасы и убрать висячие ссылки (plain text)."""
    skip = skip_stems if skip_stems is not None else _SKIP_STEMS
    existing = {p.name for p in out_dir.glob("*.md")}
    report = RemediateReport()
    for p in sorted(out_dir.glob("*.md")):
        if p.stem in skip:
            continue
        text = p.read_text(encoding="utf-8")
        new_text, remediated, stripped = _remediate_fence_stripped(text, existing, alias)
        if remediated or stripped:
            p.write_text(new_text, encoding="utf-8")
            report.files_changed += 1
            report.links_remediated += remediated
            report.links_stripped += stripped
    return report
