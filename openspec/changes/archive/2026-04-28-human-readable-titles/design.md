## Context

`convert.py` converts 25K+ HTML pages from `.hbk` archives to `.md`. Current filename derivation uses `archive_path_to_filename()` which encodes the archive directory path as double-underscore-separated segments (e.g., `objects__Global_context__methods__catalog1566__CanReadXML1628.md`). This is stable and collision-free but unreadable.

Content structure today:
```
**↑** [Главная](_index.md) › [Объекты] › ...   ← breadcrumb (line 1)
                                                  ← blank line
# Глобальный контекст.ВозможностьЧтенияXML       ← H1 (line 3)
```

The `archive_index` (path → filename map) is built before any HTML is parsed, which is why titles are unavailable at filename-derivation time. This is the core architectural constraint.

Primary consumers: Obsidian (human browsing, file-list search) and a RAG/qmd pipeline (agent chunk retrieval where filename appears as chunk metadata).

## Goals / Non-Goals

**Goals:**

- `.md` filenames derived from `title_ru` (human-readable, Obsidian searchable)
- H1 title as first line of every content file (RAG chunker sees title immediately)
- Single `title:` frontmatter field for programmatic extraction by agents
- Correct internal link resolution maintained (all `v8help://` links still resolve)
- Fallback to path-based filename for pages with no extractable title
- Collision handling for duplicate title names

**Non-Goals:**

- English transliteration of filenames (Cyrillic fine on all target systems)
- Changing index file naming (`_index__*.md` remains path-based)
- Changing log/meta file naming (`_meta.json`, `_errors.log`, etc.)
- Performance optimization beyond what three-pass requires

## Decisions

### 1. Three-pass architecture (Pass 0 pre-scan)

Add a lightweight Pass 0 before `build_archive_index`:

```
Pass 0: quick_scan_titles(extracted_dir) → dict[rel_path_lower → title_ru]
         ↓
build_archive_index(extracted_dir, prefix, title_map) → uses title_map for naming
         ↓
convert_one(...)  ← unchanged: reads archive_index for link resolution
```

Pass 0 reads only the first 4KB of each HTML file (H1 is always in `<head>`/top of `<body>`) using a regex — no full BeautifulSoup parse. Estimated cost: ~100MB I/O for 25K files ≈ +2-3s.

**Alternative considered**: single-pass with post-rename. After conversion, read `pages_meta`, rename files, rewrite all internal links. Rejected — O(n²) link rewriting, high fragility.

**Alternative considered**: two-pass (full HTML parse twice). Same result, double memory/CPU. Rejected in favor of regex-only Pass 0.

### 2. Filename format: `title_ru` sanitized, spaces → `_`

```python
_UNSAFE = re.compile(r'[/\\:*?"<>|]')

def title_to_filename(title: str, prefix: str = "") -> str:
    name = _UNSAFE.sub("", title).replace(" ", "_").strip("._")
    if not name:
        return ""  # triggers path-based fallback
    stem = (prefix + name) if prefix else name
    return stem + ".md"
```

Examples:
- `"Глобальный контекст.ВозможностьЧтенияXML"` → `Глобальный_контекст.ВозможностьЧтенияXML.md`
- `"Строка"` → `Строка.md` (lang prefix: `lang__Строка.md` — keeps `lang__` for disambiguation from shcntx)
- No title → `objects__catalog1566__CanReadXML1628.md` (path-based fallback)

**Why keep `lang__` prefix for shlang?** The `lang__` prefix distinguishes language-reference pages from object pages that might share a name (e.g., a class named `Строка`). Removing it risks collisions between the two archives.

**Alternative considered**: `title_en`-based filenames (ASCII-only). Rejected — `title_en` is often empty or contains Russian class names in parentheses. `title_ru` is always populated for shcntx pages.

### 3. H1 first, breadcrumb second

Change `inject_breadcrumb_into_content` injection order. Files with no frontmatter (current state after R4) start with H1; breadcrumb inserts after H1 + blank line:

```
# Глобальный контекст.ВозможностьЧтенияXML

**↑** [Главная](_index.md) › [Объекты] › ...

... content body ...
```

Detection: find first `# ` line, insert breadcrumb after it + blank line, rather than before.

**Rationale**: RAG chunkers treat first non-blank line as semantic title. Obsidian "Show inline title" shows H1 in editor — breadcrumb below is still navigable. No information loss.

### 4. Restore `title:` frontmatter field only

Re-enable single field in `build_frontmatter()`. R4 removed all frontmatter to reduce tokens; restoring just `title:` adds ~15 tokens per file — negligible per-file but meaningful for RAG metadata extraction:

```yaml
---
title: "Глобальный контекст.ВозможностьЧтенияXML"
---
```

Agents can `grep -l "title:" file.md` or parse YAML without reading full content.

**Alternative considered**: restore full frontmatter (R4 rollback). Rejected — full frontmatter adds `source_path`, `hbk_source`, `hbk_version`, `availability` (~60-80 tokens). `title:` alone is sufficient for identification.

### 5. Collision handling: existing `disambiguate()` unchanged

`disambiguate(name, used_names)` already adds `-2`, `-3` suffixes. Title-based names pass through the same function. No special logic needed. The `used_names` set accumulates across both shcntx and shlang archives (unchanged behavior).

### 6. Pass 0 regex for title extraction

```python
_H1_RE = re.compile(
    r'<h1[^>]*class=["\']V8SH_pagetitle["\'][^>]*>(.*?)</h1>',
    re.DOTALL | re.IGNORECASE,
)

def quick_extract_title(path: Path) -> str:
    raw = path.read_bytes()[:4096]
    text = raw.decode("utf-8-sig", errors="replace")
    m = _H1_RE.search(text)
    if not m:
        return ""
    # Strip HTML tags from match
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()
```

No BeautifulSoup needed for Pass 0. PAGETITLE_SPLIT_RE not applied — Pass 0 returns raw H1 text; `title_to_filename` uses the full text as-is (dots, parentheses stripped only of unsafe chars).

## Risks / Trade-offs

- **BREAKING change** — All existing path-based filenames change. Any external note in Obsidian that links to `objects__catalog1566__...md` breaks. **Mitigation**: document in README; vault is always regenerated from source with `--clean`.

- **Cyrillic filenames** — Work on Windows 10+, Linux ext4, macOS APFS, modern Obsidian mobile. Risk on old network shares (SMB with legacy code page). **Mitigation**: acceptable for target use case; document requirement.

- **Title collisions across archives** — If a shcntx class page and a shlang page both resolve to `Строка.md`. **Mitigation**: `lang__` prefix preserved for shlang prevents this specific collision class.

- **Titles with only special chars** — Edge case: title is `"<br>"` or similar → `title_to_filename` returns `""` → path-based fallback activates. Logged in `_truncated.log` (reuse existing log).

- **Pass 0 reads 4KB but title > 4KB from file start** — Extremely unlikely (H1 in first few hundred bytes of any HTML). **Mitigation**: increase to 8KB if tests reveal failures; add fallback to full read.

## Migration Plan

Not applicable — tool generates vault fresh from `.hbk` on each run. Breaking change is fully contained: regenerate with `--clean`, existing vault replaced. No incremental migration needed.

## Open Questions

- Should `lang__` prefix be kept in title-based names, or is collision risk low enough to drop it? **Decision: keep `lang__` for now**, revisit if user reports naming confusion.
- Should `_truncated.log` log title-based fallbacks (pages that got path-based name due to empty title)? **Decision: yes**, reuse existing log, add fallback reason column.
