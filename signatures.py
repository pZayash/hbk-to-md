"""BSL-сигнатуры: парсинг из Markdown и вставка в vault-файлы."""
from __future__ import annotations

import re
from pathlib import Path

from convert import PRIMITIVE_TYPE_STEMS

# ── Regex ──────────────────────────────────────────────────────────────────────

_TYPE_LINK_RE = re.compile(r'\[([^\]]+)\]\(((?:[^)(]|\([^)]*\))*)\)')
_H1_RE = re.compile(r'(?m)^#\s+(.+)$')
_SYNTAX_RE = re.compile(r'(?m)^Синтаксис:[^\n]*$')
_VARIANT_RE = re.compile(r'(?m)^Вариант синтаксиса:.*$')
_USAGE_SECTION_RE = re.compile(r'(?m)^Использование:[^\n]*$')
_TYPE_RE = re.compile(r'(?m)^Тип:\s*(.+)')
_READONLY_RE = re.compile(r'(?m)^(Только чтение|Чтение и запись)')
_PARAM_BLOCK_RE = re.compile(r'(?m)^(<[^>]+>)\s*\([^)]+\)\s*$')
_SYNTAX_CALL_RE = re.compile(r'^(Новый\s+)?([^\s(]+)\(([^)]*)\)\s*$')
_SIG_STRIP_RE = re.compile(r'(?s)\n?<!-- signature:start -->.*?<!-- signature:end -->\n?')

_SECTION_END_RE = re.compile(
    r'(?m)^(?:Синтаксис|Параметры|Возвращаемое значение|Описание варианта метода'
    r'|Описание|Доступность|Использование в версии|Использование'
    r'|Вариант синтаксиса|См\. также):[^\n]*$'
)


# ── Primitive-type check ───────────────────────────────────────────────────────

def is_primitive(link: str) -> bool:
    """True if link targets a primitive-type page (should not generate a graph edge)."""
    stem = link[:-3] if link.endswith(".md") else link
    stem = stem.rsplit("/", 1)[-1]
    return stem in PRIMITIVE_TYPE_STEMS or stem.startswith("lang__def_")


# ── Token parsing ──────────────────────────────────────────────────────────────

def parse_type_tokens(type_line: str) -> list[tuple[str, str]]:
    """Parse a 'Тип:' value into (name, link_or_empty) tokens."""
    line = type_line.strip().rstrip('.')
    tokens: list[tuple[str, str]] = []
    pos = 0
    for m in _TYPE_LINK_RE.finditer(line):
        gap = line[pos:m.start()].strip(', \t')
        if gap:
            tokens.append((gap, ""))
        tokens.append((m.group(1), m.group(2)))
        pos = m.end()
    remaining = line[pos:].strip(', \t')
    if remaining:
        tokens.append((remaining, ""))
    return tokens


def render_type_tokens(tokens: list[tuple[str, str]]) -> str:
    """Format tokens as [`Name`](link) | [`Name2`](link2) or `Name`."""
    parts: list[str] = []
    for name, link in tokens:
        if link and is_primitive(link):
            parts.append(f"`{name}`")
        else:
            parts.append(f"[`{name}`]({link})" if link else f"`{name}`")
    return " | ".join(parts)


# ── Section helpers ────────────────────────────────────────────────────────────

def _next_section_start(block: str, from_pos: int) -> int:
    m = _SECTION_END_RE.search(block, from_pos)
    return m.start() if m else len(block)


def _get_section_content(block: str, section_name: str) -> str | None:
    header = re.compile(rf'(?m)^{re.escape(section_name)}:[^\n]*$')
    m = header.search(block)
    if not m:
        return None
    start = m.end()
    end = _next_section_start(block, start + 1)
    return block[start:end].strip()


# ── Page kind detection ────────────────────────────────────────────────────────

def detect_page_kind(text: str) -> str | None:
    """Return 'method', 'property', 'ctor', or None."""
    if _SYNTAX_RE.search(text):
        m = re.search(r'(?m)^Синтаксис:\s*\n+([^\n]+)', text)
        if m and m.group(1).strip().startswith("Новый "):
            return "ctor"
        return "method"
    if _USAGE_SECTION_RE.search(text) and _READONLY_RE.search(text):
        return "property"
    if _TYPE_RE.search(text):
        return "property"
    return None


# ── Method / ctor extraction ───────────────────────────────────────────────────

def _extract_param_type_map(block: str) -> dict[str, list[tuple[str, str]]]:
    params_content = _get_section_content(block, "Параметры")
    if not params_content:
        return {}
    result: dict[str, list[tuple[str, str]]] = {}
    param_starts = [(m.start(), m.group(1)) for m in _PARAM_BLOCK_RE.finditer(params_content)]
    for i, (start, pname) in enumerate(param_starts):
        end = param_starts[i + 1][0] if i + 1 < len(param_starts) else len(params_content)
        param_block = params_content[start:end]
        m_type = _TYPE_RE.search(param_block)
        if m_type:
            result[pname] = parse_type_tokens(m_type.group(1))
    return result


def _extract_return_tokens(block: str) -> list[tuple[str, str]] | None:
    m_ret = re.search(r'(?m)^Возвращаемое значение:', block)
    if not m_ret:
        return None
    m_type = _TYPE_RE.search(block, m_ret.end())
    if not m_type:
        return None
    return parse_type_tokens(m_type.group(1))


def _build_one_sig(block: str) -> str | None:
    m = re.search(r'(?m)^Синтаксис:\s*\n+([^\n]+)', block)
    if not m:
        return None
    syntax_line = m.group(1).strip()
    m_call = _SYNTAX_CALL_RE.match(syntax_line)
    if not m_call:
        return None
    is_ctor = bool(m_call.group(1))
    method_name = m_call.group(2)
    params_raw = m_call.group(3)
    param_names = [p.strip() for p in params_raw.split(",") if p.strip()] if params_raw.strip() else []

    param_type_map = _extract_param_type_map(block)
    param_parts: list[str] = []
    for pname in param_names:
        tokens = param_type_map.get(pname)
        if tokens:
            param_parts.append(f"`{pname}`: {render_type_tokens(tokens)}")
        else:
            param_parts.append(f"`{pname}`")

    ret_part = ""
    if not is_ctor:
        ret_tokens = _extract_return_tokens(block)
        if ret_tokens:
            ret_part = f" → {render_type_tokens(ret_tokens)}"

    return f"`{method_name}`({', '.join(param_parts)}){ret_part}"


def extract_method_signatures(text: str) -> list[str]:
    """Return one BSL signature string per syntax variant."""
    if _VARIANT_RE.search(text):
        parts = _VARIANT_RE.split(text)
        results: list[str] = []
        for part in parts[1:]:
            sig = _build_one_sig(part)
            if sig:
                results.append(sig)
        return results
    sig = _build_one_sig(text)
    return [sig] if sig else []


# ── Property extraction ────────────────────────────────────────────────────────

def extract_property_signature(text: str) -> str | None:
    """Return BSL signature string for a property page, or None."""
    m_h1 = _H1_RE.search(text)
    if not m_h1:
        return None
    h1_title = m_h1.group(1).strip()
    prop_name = h1_title.rsplit(".", 1)[-1].strip()

    m_type = _TYPE_RE.search(text)
    if not m_type:
        return None
    tokens = parse_type_tokens(m_type.group(1))
    if not tokens:
        return None
    return f"`{prop_name}`: {render_type_tokens(tokens)}"


# ── Orchestration ──────────────────────────────────────────────────────────────

def build_signature_block(text: str) -> str | None:
    """Build the full signature block to inject, or None to skip this page."""
    kind = detect_page_kind(text)
    if kind is None:
        return None
    if kind in ("method", "ctor"):
        sigs = extract_method_signatures(text)
        return "\n\n".join(sigs) if sigs else None
    if kind == "property":
        return extract_property_signature(text)
    return None


# ── File injection ─────────────────────────────────────────────────────────────

def inject_signature_into_content(filepath: Path, signature_block: str) -> bool:
    """Insert/replace BSL signature block in file. Returns True if file changed."""
    text = filepath.read_text(encoding="utf-8")

    # Strip existing tagged block before re-inserting
    stripped = _SIG_STRIP_RE.sub("", text)
    lines = stripped.splitlines()

    h1_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if h1_idx is None:
        return False

    bc_idx: int | None = None
    for i in range(h1_idx + 1, min(h1_idx + 15, len(lines))):
        if lines[i].startswith("**↑**"):
            bc_idx = i
            break

    anchor = bc_idx if bc_idx is not None else h1_idx

    skip = anchor + 1
    while skip < len(lines) and not lines[skip].strip():
        skip += 1

    tagged_lines = [
        "<!-- signature:start -->",
        *signature_block.splitlines(),
        "<!-- signature:end -->",
    ]
    new_lines = lines[:anchor + 1] + [""] + tagged_lines + [""] + lines[skip:]
    new_text = "\n".join(new_lines).rstrip() + "\n"
    if new_text == text:
        return False
    filepath.write_text(new_text, encoding="utf-8")
    return True
