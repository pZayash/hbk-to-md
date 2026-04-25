"""CLI-конвертер .hbk (1С) → плоский каталог .md.

См. README.md для CLI и формата выходных файлов.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify as md_convert
from onec_dtools.container_reader import ContainerReader


MAX_FILENAME = 200
LANG_PREFIX = "lang__"
SHCNTX_NAME = "shcntx_ru"
SHLANG_NAME = "shlang_ru"
BREADCRUMB_SEPARATOR = " › "
ALPHA_GROUP_THRESHOLD = 50
INDEX_PREFIX = "_index"
BREADCRUMB_MARKER = "**↑** [Главная]"

SEGMENT_TITLES = {
    "methods": "Методы",
    "properties": "Свойства",
    "events": "События",
    "ctors": "Конструкторы",
    "objects": "Объекты",
    "tables": "Таблицы",
    "lang": "Встроенный язык 1С",
    "Global context": "Глобальный контекст",
}

V8HELP_RE = re.compile(r"^v8help://(SyntaxHelperContext|SyntaxHelperLanguage)/(.+?)(?:#(.+))?$", re.IGNORECASE)
BROKEN_HREF_RE = re.compile(r'href\s*=\s*http[^\s"\'>]*\?[A-Za-z]+\s*=\s*"', re.IGNORECASE)
VERSION_FROM_PATH_RE = re.compile(r"[/\\\\]1cv8[/\\\\](\d+\.\d+\.\d+\.\d+)[/\\\\]bin[/\\\\]", re.IGNORECASE)
AVAILABILITY_RE = re.compile(r"(8\.\d+(?:\.\d+)?)")
PAGETITLE_SPLIT_RE = re.compile(r"^(.*)\s*\(([^()]*)\)\s*$")


# ---------- Распаковка ---------------------------------------------------

def extract_hbk(hbk_path: Path, dest: Path) -> None:
    """Распаковать .hbk → каталог dest c HTML-страницами.

    .hbk = V8 storage container. Внутри среди прочего файл `FileStorage` —
    обычный ZIP с HTML-страницами справки. Распаковка двухступенчатая:
    1) onec_dtools.ContainerReader разбирает V8 storage (deflate=False, recursive=True)
    2) zipfile разворачивает FileStorage в dest
    """
    dest.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hbk-v8-") as v8_tmp:
        v8_unpack = Path(v8_tmp) / "v8"
        with hbk_path.open("rb") as f:
            ContainerReader(f).extract(str(v8_unpack), deflate=False, recursive=True)
        file_storage = v8_unpack / "FileStorage"
        if not file_storage.exists():
            raise RuntimeError(
                f"В контейнере {hbk_path.name} нет 'FileStorage' (есть: "
                f"{sorted(p.name for p in v8_unpack.iterdir())})"
            )
        with zipfile.ZipFile(file_storage, mode="r", metadata_encoding="utf-8") as zf:
            zf.extractall(dest)


def derive_version(hbk_path: Path) -> str:
    """Вытащить версию из .../1cv8/X.Y.Z.W/bin/... либо вернуть 'unknown'."""
    m = VERSION_FROM_PATH_RE.search(str(hbk_path))
    return m.group(1) if m else "unknown"


def prepare_output(out: Path, clean: bool) -> None:
    """Создать --out пустым; при clean — снести содержимое."""
    if out.exists():
        non_empty = any(out.iterdir())
        if non_empty:
            if not clean:
                raise SystemExit(f"--out '{out}' не пуст; используйте --clean для пересоздания")
            shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)


# ---------- Нормализация имён -------------------------------------------

def archive_path_to_filename(rel_path: str, prefix: str = "") -> str:
    """Преобразовать путь архива в плоское имя .md (без обрезки/коллизий)."""
    rel = rel_path.replace("\\", "/").lstrip("./")
    if rel.lower().endswith(".html"):
        rel = rel[: -len(".html")] + ".md"
    elif rel.lower().endswith(".htm"):
        rel = rel[: -len(".htm")] + ".md"
    elif "." not in rel.rsplit("/", 1)[-1]:
        rel = rel + ".md"
    segments = [seg.replace(" ", "_") for seg in rel.split("/") if seg]
    name = "__".join(segments)
    if prefix and not name.startswith(prefix):
        name = prefix + name
    return name


def truncate_filename(name: str, source_path: str) -> tuple[str, bool]:
    """Если имя > MAX_FILENAME — обрезать и добавить SHA1[:8] исходного пути."""
    if len(name) <= MAX_FILENAME:
        return name, False
    digest = hashlib.sha1(source_path.encode("utf-8")).hexdigest()[:8]
    suffix = f"__TRUNC_{digest}.md"
    head_len = MAX_FILENAME - len(suffix)
    if head_len < 16:
        head_len = 16
    base = name[:-3] if name.endswith(".md") else name
    return base[:head_len] + suffix, True


def disambiguate(name: str, used: set[str]) -> tuple[str, bool]:
    """Если имя уже занято — добавлять -2, -3, ..."""
    if name not in used:
        return name, False
    if name.endswith(".md"):
        base, ext = name[:-3], ".md"
    else:
        base, ext = name, ""
    n = 2
    while True:
        candidate = f"{base}-{n}{ext}"
        if candidate not in used:
            return candidate, True
        n += 1


# ---------- Парсинг HTML ------------------------------------------------

def read_html(path: Path) -> str:
    """utf-8-sig → fallback cp1251."""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1251", errors="replace")


def parse_html(content: str) -> BeautifulSoup:
    cleaned = BROKEN_HREF_RE.sub("data-broken-href=\"", content)
    return BeautifulSoup(cleaned, "lxml")


def extract_titles(soup: BeautifulSoup) -> tuple[str, str]:
    h1 = soup.find("h1", class_="V8SH_pagetitle")
    if not h1:
        return "", ""
    text = h1.get_text(strip=True)
    m = PAGETITLE_SPLIT_RE.match(text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text, ""


def extract_availability(soup: BeautifulSoup) -> str | None:
    p = soup.find("p", class_="V8SH_versionInfo")
    if not p:
        return None
    m = AVAILABILITY_RE.search(p.get_text(" ", strip=True))
    return m.group(1) if m else None


def rewrite_links(
    soup: BeautifulSoup,
    archive_index: dict[str, str],
    unresolved_log: list[tuple[str, str]],
    page_source_path: str,
) -> None:
    """Переписать v8help://... в относительные .md; убрать битые href."""
    for a in list(soup.find_all("a")):
        if a.has_attr("data-broken-href"):
            a.replace_with(NavigableString(a.get_text("", strip=False)))
            continue
        href = a.get("href")
        if not href:
            continue
        href_s = href.strip()
        if href_s.lower().startswith(("http://", "https://", "mailto:", "ftp://")):
            continue
        if href_s.startswith("#"):
            continue
        m = V8HELP_RE.match(href_s)
        if m:
            scheme, raw_target, anchor = m.group(1), m.group(2), m.group(3)
            normalized = raw_target.lstrip("/")
            if scheme.lower() == "syntaxhelpercontext":
                target_filename = archive_index.get(normalized.lower())
                if not target_filename:
                    target_filename = archive_path_to_filename(normalized)
                    unresolved_log.append((page_source_path, href_s))
            else:
                key1 = normalized.lower()
                key2 = (normalized + ".html").lower()
                target_filename = archive_index.get(key1) or archive_index.get(key2)
                if not target_filename:
                    target_filename = archive_path_to_filename(normalized, prefix=LANG_PREFIX)
                    unresolved_log.append((page_source_path, href_s))
        else:
            # Относительный (или абсолютный архивный) HTML-путь — резолвим
            # относительно каталога текущей страницы.
            path_part, _, anchor = href_s.partition("#")
            anchor = anchor or None
            path_part = path_part.split("?", 1)[0]
            if not path_part:
                continue
            base_dir = posixpath.dirname(page_source_path)
            resolved = posixpath.normpath(posixpath.join(base_dir, path_part)).lstrip("/")
            target_filename = archive_index.get(resolved.lower())
            if not target_filename:
                target_filename = archive_path_to_filename(resolved)
                unresolved_log.append((page_source_path, href_s))
        new_href = target_filename
        if anchor:
            new_href += "#" + anchor
        a["href"] = new_href


# ---------- Markdown ---------------------------------------------------

CODE_FENCE_RE = re.compile(r"(```[\s\S]*?```)")
MD_LINK_TEXT_RE = re.compile(r"(?<!\\)\[((?:[^\[\]\\]|\\.)*?)\]\(")
METHODOLOGICAL_LINE_RE = re.compile(
    r'(?mi)^\s*(?:\[)?\s*Методическая информация(?:\]\([^)]*1centerprise\.com/devlinks[^)]*\))?\s*$'
)


def _escape_angles_in_link_text(md: str) -> str:
    """Экранировать `<`/`>` в тексте `[...]` MD-ссылок: иначе Obsidian
    парсит `<word>` как HTML-тег и ломает разметку линка.
    Code-блоки (```...```) не трогаем.
    """
    parts = []
    for chunk in CODE_FENCE_RE.split(md):
        if chunk.startswith("```"):
            parts.append(chunk)
            continue
        parts.append(MD_LINK_TEXT_RE.sub(
            lambda m: "[" + m.group(1).replace("<", r"\<").replace(">", r"\>") + "](",
            chunk,
        ))
    return "".join(parts)


def to_markdown(soup: BeautifulSoup) -> str:
    body = soup.body if soup.body else soup
    html = body.decode_contents() if hasattr(body, "decode_contents") else str(body)
    md = md_convert(html, strip=["script", "style"], heading_style="ATX", bullets="-")
    md = _escape_angles_in_link_text(md)
    return cleanup_markdown_noise(md)


def cleanup_markdown_noise(md: str) -> str:
    lines = md.splitlines()
    cleaned: list[str] = []
    for line in lines:
        if "1centerprise.com/devlinks" in line:
            continue
        if METHODOLOGICAL_LINE_RE.match(line):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def yaml_escape(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_frontmatter(meta: dict) -> str:
    order = ("title_ru", "title_en", "source_path", "hbk_source", "hbk_version", "availability")
    lines = ["---"]
    for key in order:
        if key not in meta:
            continue
        val = meta[key]
        if val is None:
            continue
        lines.append(f"{key}: {yaml_escape(str(val))}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def write_md(out_dir: Path, filename: str, frontmatter: str, body: str) -> None:
    (out_dir / filename).write_text(frontmatter + body.strip() + "\n", encoding="utf-8")


# ---------- Pipeline ---------------------------------------------------

@dataclass
class Stats:
    total: int = 0
    converted: int = 0
    failed: int = 0
    truncated: int = 0
    collisions: int = 0
    unresolved: int = 0
    index_files_generated: int = 0
    breadcrumbs_added: int = 0
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None

    def as_dict(self) -> dict:
        d = self.__dict__.copy()
        d["duration_sec"] = round((self.finished_at or time.time()) - self.started_at, 2)
        return d


_HTML_SNIFF_HEADS = (b"<html", b"<!doctype", b"<HTML", b"<!DOCTYPE")
_NON_HTML_EXT = {".st", ".data", ".png", ".jpg", ".jpeg", ".gif", ".css", ".js", ".bin"}


def _looks_like_html(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            head = f.read(64)
    except OSError:
        return False
    if head.startswith(b"\xef\xbb\xbf"):
        head = head[3:]
    head_lower = head.lower()
    return head_lower.startswith(b"<html") or head_lower.startswith(b"<!doctype")


def iter_html(extracted_dir: Path) -> Iterable[Path]:
    for p in extracted_dir.rglob("*"):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in (".html", ".htm"):
            yield p
            continue
        if ext in _NON_HTML_EXT:
            continue
        if ext == "" and _looks_like_html(p):
            yield p


def build_archive_index(extracted_dir: Path, prefix: str) -> dict[str, str]:
    """Карта lookup-key → target_filename (без обрезки/disambig).

    Для shcntx (prefix=""): ключ = rel_path.lower() (например, 'objects/x/y.html').
    Для shlang (prefix='lang__'): кроме rel_path.lower() добавляется stem.lower()
    ('def_string'), т.к. v8help-ссылки на язык приходят без расширения.
    """
    index: dict[str, str] = {}
    for html in iter_html(extracted_dir):
        rel = html.relative_to(extracted_dir).as_posix()
        target = archive_path_to_filename(rel, prefix=prefix)
        index[rel.lower()] = target
        if prefix == LANG_PREFIX:
            stem = rel.rsplit(".", 1)[0]
            index[stem.lower()] = target
    return index


def convert_one(
    html_path: Path,
    rel_path: str,
    out_dir: Path,
    archive_index: dict[str, str],
    used_names: set[str],
    hbk_source: str,
    hbk_version: str,
    prefix: str,
    logs: dict[str, list],
    stats: Stats,
    pages_meta: dict[str, dict],
    archive_lookup_final: dict[str, str],
) -> None:
    target = archive_path_to_filename(rel_path, prefix=prefix)
    final_name, was_truncated = truncate_filename(target, rel_path)
    if was_truncated:
        logs["truncated"].append((rel_path, final_name))
        stats.truncated += 1
    final_name, was_collision = disambiguate(final_name, used_names)
    if was_collision:
        logs["collisions"].append((rel_path, final_name))
        stats.collisions += 1
    used_names.add(final_name)

    content = read_html(html_path)
    soup = parse_html(content)
    rewrite_links(soup, archive_index, logs["unresolved"], rel_path)
    title_ru, title_en = extract_titles(soup)
    availability = extract_availability(soup)

    # Сносим оригинальный V8SH_pagetitle h1 (заменим на чистый H1 из title_ru).
    # V8SH_title удаляем только если он дублирует pagetitle (на страницах классов
    # parent == self); на страницах методов он несёт parent-контекст — оставляем.
    pagetitle_el = soup.find(class_="V8SH_pagetitle")
    pagetitle_text = pagetitle_el.get_text(strip=True) if pagetitle_el else ""
    if pagetitle_el:
        pagetitle_el.decompose()
    title_el = soup.find(class_="V8SH_title")
    if title_el and pagetitle_text and title_el.get_text(strip=True) == pagetitle_text:
        title_el.decompose()

    fm = {
        "title_ru": title_ru,
        "title_en": title_en,
        "source_path": rel_path,
        "hbk_source": hbk_source,
        "hbk_version": hbk_version,
    }
    if availability:
        fm["availability"] = availability
    body = to_markdown(soup)
    heading = title_ru or title_en
    if heading:
        body = f"# {heading}\n\n" + body.lstrip()
    write_md(out_dir, final_name, "", body)
    pages_meta[final_name] = fm
    rel_lower = rel_path.lower()
    archive_lookup_final[rel_lower] = final_name
    if prefix == LANG_PREFIX:
        stem = rel_lower.rsplit(".", 1)[0]
        archive_lookup_final[stem] = final_name
        archive_lookup_final[f"lang/{rel_lower}"] = final_name
        archive_lookup_final[f"lang/{stem}"] = final_name


def _convert_archive(
    extracted_dir: Path,
    out_dir: Path,
    prefix: str,
    hbk_source: str,
    hbk_version: str,
    archive_index: dict[str, str],
    used_names: set[str],
    logs: dict[str, list],
    stats: Stats,
    pages_meta: dict[str, dict],
    archive_lookup_final: dict[str, str],
) -> None:
    for html_path in iter_html(extracted_dir):
        rel = html_path.relative_to(extracted_dir).as_posix()
        stats.total += 1
        try:
            convert_one(
                html_path=html_path,
                rel_path=rel,
                out_dir=out_dir,
                archive_index=archive_index,
                used_names=used_names,
                hbk_source=hbk_source,
                hbk_version=hbk_version,
                prefix=prefix,
                logs=logs,
                stats=stats,
                pages_meta=pages_meta,
                archive_lookup_final=archive_lookup_final,
            )
            stats.converted += 1
        except Exception as exc:
            stats.failed += 1
            logs["errors"].append((rel, repr(exc)))


# ---------- Pipeline post-processing -----------------------------------


@dataclass
class TreeNode:
    prefix: str
    segment: str
    title: str = ""
    content_filename: str | None = None
    children: dict[str, "TreeNode"] = field(default_factory=dict)
    page_count: int = 0


def source_prefix(path: str) -> str:
    path = path.replace("\\", "/").lstrip("./")
    if path.lower().endswith(".html"):
        return path[: -len(".html")]
    if path.lower().endswith(".htm"):
        return path[: -len(".htm")]
    return path


def build_hierarchy(archive_index: dict[str, str], pages_meta: dict[str, dict]) -> TreeNode:
    root = TreeNode(prefix="", segment="")
    for filename, meta in pages_meta.items():
        src = meta.get("source_path")
        if not src:
            continue
        prefix = source_prefix(src)
        if "/" not in prefix and str(meta.get("hbk_source")) == SHLANG_NAME:
            prefix = f"lang/{prefix}"
        segments = [s for s in prefix.split("/") if s]
        node = root
        current_prefix: list[str] = []
        for seg in segments:
            current_prefix.append(seg)
            full_prefix = "/".join(current_prefix)
            child = node.children.get(seg)
            if child is None:
                child = TreeNode(prefix=full_prefix, segment=seg)
                node.children[seg] = child
            node = child
        node.content_filename = filename
        node.title = str(meta.get("title_ru") or meta.get("title_en") or node.title or node.segment)
    return root


def propagate_titles(node: TreeNode, pages_meta: dict[str, dict]) -> None:
    for child in node.children.values():
        propagate_titles(child, pages_meta)
    if node.prefix == "":
        return
    if node.content_filename:
        meta = pages_meta.get(node.content_filename, {})
        node.title = str(meta.get("title_ru") or meta.get("title_en") or node.title or node.segment)
    elif not node.title:
        inferred = infer_title_from_children(node)
        node.title = inferred or SEGMENT_TITLES.get(node.segment, node.segment)


def infer_title_from_children(node: TreeNode) -> str:
    """Вывести человекочитаемый заголовок internal-узла из дочерних title.

    Важно для `tables/catalogNN`, где собственной content-страницы нет.
    """
    if not node.children:
        return ""
    parent_segment = node.prefix.rsplit("/", 2)[-2] if "/" in node.prefix else ""
    if parent_segment != "tables" or not re.fullmatch(r"catalog\d+", node.segment):
        return ""
    child_titles = [c.title.strip() for c in node.children.values() if c.title and "." in c.title]
    if not child_titles:
        return ""
    changes_like = sum(1 for title in child_titles if title.endswith(".Изменения"))
    if changes_like >= max(3, len(child_titles) // 2):
        return "ТаблицыИзменений"
    split_titles = [title.split(".") for title in child_titles]
    common_parts: list[str] = []
    for idx in range(min(len(parts) for parts in split_titles)):
        part = split_titles[0][idx]
        if all(parts[idx] == part for parts in split_titles[1:]):
            common_parts.append(part)
        else:
            break
    if common_parts:
        return simplify_catalog_title(".".join(common_parts))
    return simplify_catalog_title(child_titles[0])


def simplify_catalog_title(title: str) -> str:
    """Сократить заголовок до базового типа (без .<Имя ...>)."""
    marker = ".<"
    pos = title.find(marker)
    if pos > 0:
        return title[:pos]
    return title


PLACEHOLDER_SEGMENT_RE = re.compile(r"\.<[^>]+>")


def simplify_table_section_title(title: str) -> str:
    """Убрать placeholder-сегменты вида '.<Имя ...>' из table-заголовков.

    Пример:
    'БизнесПроцесс.<Имя бизнес-процесса>.Точки' -> 'БизнесПроцесс.Точки'
    """
    simplified = PLACEHOLDER_SEGMENT_RE.sub("", title)
    return simplified.strip(". ")


def compute_page_counts(node: TreeNode) -> int:
    count = 1 if node.content_filename else 0
    for child in node.children.values():
        count += compute_page_counts(child)
    node.page_count = count
    return count


def index_filename_for(prefix: str) -> str:
    if not prefix:
        return f"{INDEX_PREFIX}.md"
    stem = archive_path_to_filename(prefix)
    if stem.endswith(".md"):
        stem = stem[:-3]
    return f"{INDEX_PREFIX}__{stem}.md"


def parent_index_for(prefix: str) -> str | None:
    if not prefix:
        return None
    parts = [p for p in prefix.split("/") if p]
    if len(parts) <= 1:
        return f"{INDEX_PREFIX}.md"
    parent_prefix = "/".join(parts[:-1])
    return index_filename_for(parent_prefix)


def walk_parents(prefix: str) -> list[str]:
    parts = [p for p in prefix.split("/") if p]
    result: list[str] = []
    for i in range(1, len(parts)):
        result.append("/".join(parts[:i]))
    return result


def collect_prefix_map(root: TreeNode) -> dict[str, TreeNode]:
    out: dict[str, TreeNode] = {}
    stack = [root]
    while stack:
        node = stack.pop()
        if node.prefix:
            out[node.prefix] = node
        stack.extend(node.children.values())
    return out


def resolve_breadcrumb_target(
    prefix: str,
    archive_index: dict[str, str],
    index_filenames: set[str],
    prefix_map: dict[str, TreeNode],
) -> tuple[str, str] | None:
    key_html = prefix.lower() + ".html"
    key_plain = prefix.lower()
    content = archive_index.get(key_html) or archive_index.get(key_plain)
    if content:
        node = prefix_map.get(prefix)
        title = node.title if node and node.title else prefix.split("/")[-1]
        return content, title
    idx = index_filename_for(prefix)
    if idx in index_filenames:
        node = prefix_map.get(prefix)
        title = node.title if node and node.title else SEGMENT_TITLES.get(prefix.split("/")[-1], prefix.split("/")[-1])
        return idx, title
    return None


def render_breadcrumb(
    prefix: str,
    archive_index: dict[str, str],
    index_filenames: set[str],
    prefix_map: dict[str, TreeNode],
) -> str:
    parts = [f"{BREADCRUMB_MARKER}({INDEX_PREFIX}.md)"]
    for parent_prefix in walk_parents(prefix):
        resolved = resolve_breadcrumb_target(parent_prefix, archive_index, index_filenames, prefix_map)
        if not resolved:
            continue
        filename, title = resolved
        parts.append(f"[{title}]({filename})")
    return BREADCRUMB_SEPARATOR.join(parts)


def _sort_nodes(nodes: list[TreeNode]) -> list[TreeNode]:
    return sorted(nodes, key=lambda n: (n.title or n.segment).casefold())


def _render_links_with_groups(items: list[tuple[str, str]]) -> list[str]:
    if len(items) <= ALPHA_GROUP_THRESHOLD:
        return [f"- [{title}]({target})" for title, target in items]
    grouped: dict[str, list[tuple[str, str]]] = {}
    for title, target in items:
        head = (title[:1] if title else "#").upper()
        grouped.setdefault(head, []).append((title, target))
    lines: list[str] = []
    for letter in sorted(grouped.keys(), key=lambda x: x.casefold()):
        lines.append(f"### {letter}")
        lines.append("")
        for title, target in grouped[letter]:
            lines.append(f"- [{title}]({target})")
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def render_index(
    node: TreeNode,
    parent_index: str | None,
    archive_index: dict[str, str],
    index_filenames: set[str],
    prefix_map: dict[str, TreeNode],
) -> str:
    lines = [
        "---",
        "type: index",
        f"source_prefix: {yaml_escape(node.prefix)}",
    ]
    if parent_index:
        lines.append(f"parent_index: {yaml_escape(parent_index)}")
    lines.extend(["---", "", f"# {node.title}", ""])
    if node.content_filename:
        lines.append(f"[Содержание страницы раздела →]({node.content_filename})")
        lines.append("")
    subsections = _sort_nodes([c for c in node.children.values() if c.children])
    pages = _sort_nodes([c for c in node.children.values() if (not c.children and c.content_filename)])
    if subsections:
        lines.append(f"## Подразделы ({len(subsections)})")
        lines.append("")
        use_table_simplify = node.prefix == "tables" or node.prefix.startswith("tables/")
        subsection_items = []
        for c in subsections:
            label = simplify_table_section_title(c.title) if use_table_simplify else c.title
            target = c.content_filename if c.content_filename else index_filename_for(c.prefix)
            subsection_items.append((f"{label} ({c.page_count} страниц)", target))
        lines.extend(_render_links_with_groups(subsection_items))
        lines.append("")
    if pages:
        lines.append(f"## Страницы ({len(pages)})")
        lines.append("")
        page_items = []
        for c in pages:
            title = c.title
            page_items.append((title, c.content_filename or ""))
        lines.extend(_render_links_with_groups(page_items))
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(render_breadcrumb(node.prefix, archive_index, index_filenames, prefix_map))
    lines.append("")
    return "\n".join(lines)


def render_root_index(
    tree: TreeNode,
    hbk_version: str,
    total_pages: int,
    source_counts: dict[str, int] | None = None,
) -> str:
    lines = [
        "---",
        "type: index-root",
        f"hbk_version: {yaml_escape(hbk_version)}",
        f"total_pages: {total_pages}",
        "---",
        "",
        f"# Vault: 1С:Предприятие {hbk_version} — справка",
        "",
        f"Всего страниц: **{total_pages}**",
        "",
        "## Разделы",
        "",
    ]
    if source_counts:
        details = ", ".join(f"{name}: {count}" for name, count in sorted(source_counts.items()))
        lines.insert(9, f"По архивам: {details}")
        lines.insert(10, "")
    for child in _sort_nodes([c for c in tree.children.values() if c.page_count > 0]):
        lines.append(f"- [{child.title} ({child.page_count} страниц)]({index_filename_for(child.prefix)})")
    lines.append("")
    return "\n".join(lines)


def write_all_indexes(
    tree: TreeNode,
    out_dir: Path,
    archive_index: dict[str, str],
) -> tuple[int, set[str]]:
    count = 0
    index_filenames: set[str] = {f"{INDEX_PREFIX}.md"}
    prefix_map = collect_prefix_map(tree)
    stack = [tree]
    while stack:
        node = stack.pop()
        stack.extend(node.children.values())
        if node.prefix == "" or not node.children or node.content_filename:
            continue
        filename = index_filename_for(node.prefix)
        parent_index = parent_index_for(node.prefix)
        body = render_index(node, parent_index, archive_index, index_filenames, prefix_map)
        write_md(out_dir, filename, "", body)
        index_filenames.add(filename)
        count += 1
    return count, index_filenames


def inject_breadcrumb_into_content(filepath: Path, breadcrumb: str) -> bool:
    text = filepath.read_text(encoding="utf-8")
    text_wo_breadcrumb = re.sub(r"(?m)^\*\*↑\*\* \[Главная\].*\n\n?", "", text, count=1).lstrip("\n")
    if text_wo_breadcrumb.startswith("---\n"):
        lines = text_wo_breadcrumb.splitlines()
        fm_end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i
                break
        if fm_end is not None:
            insert_at = fm_end + 1
            body_lines = lines[insert_at:]
            new_lines = lines[:insert_at] + [breadcrumb, ""] + body_lines
            new_text = "\n".join(new_lines).rstrip() + "\n"
        else:
            new_text = f"{breadcrumb}\n\n{text_wo_breadcrumb.rstrip()}\n"
    else:
        new_text = f"{breadcrumb}\n\n{text_wo_breadcrumb.rstrip()}\n"
    if new_text == text:
        return False
    filepath.write_text(new_text, encoding="utf-8")
    return True


def render_inline_toc(node: TreeNode) -> str:
    subsections = _sort_nodes([c for c in node.children.values() if c.children])
    pages = _sort_nodes([c for c in node.children.values() if (not c.children and c.content_filename)])
    if not subsections and not pages:
        return ""
    lines = ["## Оглавление", ""]
    use_table_simplify = node.prefix == "tables" or node.prefix.startswith("tables/")
    if subsections:
        lines.append(f"### Подразделы ({len(subsections)})")
        lines.append("")
        subsection_items = []
        for c in subsections:
            label = simplify_table_section_title(c.title) if use_table_simplify else c.title
            target = c.content_filename if c.content_filename else index_filename_for(c.prefix)
            subsection_items.append((f"{label} ({c.page_count} страниц)", target))
        lines.extend(_render_links_with_groups(subsection_items))
        lines.append("")
    if pages:
        lines.append(f"### Страницы ({len(pages)})")
        lines.append("")
        page_items = [(c.title, c.content_filename or "") for c in pages]
        lines.extend(_render_links_with_groups(page_items))
        lines.append("")
    return "\n".join(lines).rstrip()


def inject_inline_toc_into_content(filepath: Path, toc: str) -> bool:
    if not toc:
        return False
    text = filepath.read_text(encoding="utf-8")
    text = re.sub(r"(?s)\n?<!-- toc:start -->.*?<!-- toc:end -->\n?", "\n", text).rstrip()
    new_text = f"{text}\n\n<!-- toc:start -->\n{toc}\n<!-- toc:end -->\n"
    if new_text == filepath.read_text(encoding="utf-8"):
        return False
    filepath.write_text(new_text, encoding="utf-8")
    return True


def inject_all_breadcrumbs(
    tree: TreeNode,
    out_dir: Path,
    archive_index: dict[str, str],
    index_filenames: set[str],
) -> int:
    updated = 0
    prefix_map = collect_prefix_map(tree)
    stack = [tree]
    while stack:
        node = stack.pop()
        stack.extend(node.children.values())
        if not node.content_filename:
            continue
        filepath = out_dir / node.content_filename
        if not filepath.exists():
            continue
        if node.children:
            toc = render_inline_toc(node)
            inject_inline_toc_into_content(filepath, toc)
        breadcrumb = render_breadcrumb(node.prefix, archive_index, index_filenames, prefix_map)
        if inject_breadcrumb_into_content(filepath, breadcrumb):
            updated += 1
    return updated


def build_toc(
    out_dir: Path,
    archive_index: dict[str, str],
    pages_meta: dict[str, dict],
    hbk_version: str,
    total_pages: int,
) -> tuple[TreeNode, set[str], int]:
    tree = build_hierarchy(archive_index, pages_meta)
    propagate_titles(tree, pages_meta)
    compute_page_counts(tree)
    index_count, index_filenames = write_all_indexes(tree, out_dir, archive_index)
    source_counts: dict[str, int] = {}
    for meta in pages_meta.values():
        src = str(meta.get("hbk_source") or "")
        if not src:
            continue
        source_counts[src] = source_counts.get(src, 0) + 1
    write_md(
        out_dir,
        f"{INDEX_PREFIX}.md",
        "",
        render_root_index(tree, hbk_version, total_pages, source_counts=source_counts),
    )
    return tree, index_filenames, index_count + 1


def inject_breadcrumbs(out_dir: Path, archive_index: dict[str, str], tree: TreeNode, index_filenames: set[str]) -> int:
    return inject_all_breadcrumbs(tree, out_dir, archive_index, index_filenames)


def write_logs(out_dir: Path, logs: dict[str, list], stats: Stats, params: dict) -> None:
    if logs["truncated"]:
        (out_dir / "_truncated.log").write_text(
            "\n".join(f"{a}\t{b}" for a, b in logs["truncated"]) + "\n",
            encoding="utf-8",
        )
    if logs["collisions"]:
        (out_dir / "_collisions.log").write_text(
            "\n".join(f"{a}\t{b}" for a, b in logs["collisions"]) + "\n",
            encoding="utf-8",
        )
    if logs["unresolved"]:
        stats.unresolved = len(logs["unresolved"])
        (out_dir / "_unresolved.log").write_text(
            "\n".join(f"{a}\t{b}" for a, b in logs["unresolved"]) + "\n",
            encoding="utf-8",
        )
    if logs["errors"]:
        (out_dir / "_errors.log").write_text(
            "\n".join(f"{a}\t{b}" for a, b in logs["errors"]) + "\n",
            encoding="utf-8",
        )
    stats.finished_at = time.time()
    meta = {"params": params, "stats": stats.as_dict()}
    (out_dir / "_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Конвертер .hbk (1С) → плоский каталог .md")
    parser.add_argument("--hbk", required=True, type=Path, help="Путь к shcntx_ru.hbk")
    parser.add_argument("--lang-hbk", type=Path, default=None, help="Путь к shlang_ru.hbk (опционально)")
    parser.add_argument("--out", required=True, type=Path, help="Выходной каталог")
    parser.add_argument("--version", default=None, help="Версия платформы (если не указана — выводится из пути)")
    parser.add_argument("--clean", action="store_true", help="Снести --out перед конвертацией")
    args = parser.parse_args(argv)

    out_dir: Path = args.out.resolve()
    prepare_output(out_dir, args.clean)

    hbk_version = args.version or derive_version(args.hbk)
    params = {
        "hbk": str(args.hbk),
        "lang_hbk": str(args.lang_hbk) if args.lang_hbk else None,
        "out": str(out_dir),
        "version": hbk_version,
        "clean": args.clean,
    }
    stats = Stats()
    logs: dict[str, list] = {"truncated": [], "collisions": [], "unresolved": [], "errors": []}
    used_names: set[str] = set()
    pages_meta: dict[str, dict] = {}
    archive_lookup_final: dict[str, str] = {}

    with tempfile.TemporaryDirectory(prefix="hbk-to-md-") as tmp:
        tmp_root = Path(tmp)
        ctx_dir = tmp_root / "shcntx"
        lang_dir = tmp_root / "shlang"

        print(f"[hbk-to-md] extract {args.hbk.name}", flush=True)
        extract_hbk(args.hbk, ctx_dir)
        archive_index = build_archive_index(ctx_dir, prefix="")
        if args.lang_hbk:
            print(f"[hbk-to-md] extract {args.lang_hbk.name}", flush=True)
            extract_hbk(args.lang_hbk, lang_dir)
            archive_index.update(build_archive_index(lang_dir, prefix=LANG_PREFIX))

        print(f"[hbk-to-md] convert shcntx_ru", flush=True)
        _convert_archive(
            ctx_dir, out_dir, prefix="", hbk_source=SHCNTX_NAME, hbk_version=hbk_version,
            archive_index=archive_index, used_names=used_names, logs=logs, stats=stats,
            pages_meta=pages_meta, archive_lookup_final=archive_lookup_final,
        )

        if args.lang_hbk:
            print(f"[hbk-to-md] convert shlang_ru", flush=True)
            _convert_archive(
                lang_dir, out_dir, prefix=LANG_PREFIX, hbk_source=SHLANG_NAME, hbk_version=hbk_version,
                archive_index=archive_index, used_names=used_names, logs=logs, stats=stats,
                pages_meta=pages_meta, archive_lookup_final=archive_lookup_final,
            )

    tree, index_filenames, index_count = build_toc(
        out_dir=out_dir,
        archive_index=archive_lookup_final,
        pages_meta=pages_meta,
        hbk_version=hbk_version,
        total_pages=stats.converted,
    )
    stats.index_files_generated = index_count
    stats.breadcrumbs_added = inject_breadcrumbs(out_dir, archive_lookup_final, tree, index_filenames)

    write_logs(out_dir, logs, stats, params)
    print(
        f"[hbk-to-md] done: total={stats.total} converted={stats.converted} "
        f"failed={stats.failed} truncated={stats.truncated} "
        f"collisions={stats.collisions} unresolved={stats.unresolved} "
        f"index_files={stats.index_files_generated} breadcrumbs={stats.breadcrumbs_added} "
        f"duration={stats.as_dict()['duration_sec']}s",
        flush=True,
    )
    return 0 if stats.failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
