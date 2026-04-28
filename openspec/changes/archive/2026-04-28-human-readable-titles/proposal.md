## Why

Converted `.md` files have cryptic path-derived filenames (e.g., `objects__Global_context__methods__catalog1566__CanReadXML1628.md`) that reveal nothing about content. Additionally, each file opens with a breadcrumb navigation line — not the title — so the first semantic signal is on line 3. Both humans browsing in Obsidian and agents processing files in a RAG pipeline cannot identify what a file is about without opening it and reading past the breadcrumb.

## What Changes

- **BREAKING** — Filename derivation switches from archive path → `title_ru`-based name (e.g., `Глобальный_контекст.ВозможностьЧтенияXML.md`). Any externally saved links to the old path-based filenames will break. Vault must be regenerated with `--clean`.
- A new lightweight pre-scan pass (Pass 0) reads only the H1 from each HTML page before building `archive_index`, enabling title-based filenames while preserving correct internal link resolution.
- File content order changes: `# H1 title` becomes the first line, breadcrumb moves below it.
- A single `title:` field is restored to frontmatter for programmatic access by agents.
- Fallback: pages with no extractable title retain path-based filename.

## Capabilities

### New Capabilities

- `title-based-filenames`: Pre-scan HTML pages to extract titles before building archive_index; derive `.md` filenames from `title_ru` (sanitized, collision-handled) instead of archive path.

### Modified Capabilities

- `hbk-to-md-converter`: Filename derivation behavior changes (path-based → title-based); content structure changes (H1 first, then breadcrumb); frontmatter gains `title:` field.

## Impact

- `convert.py`: `archive_path_to_filename()` remains for fallback; new `title_to_filename()` + `quick_scan_titles()` added; `build_archive_index()` gains optional title map parameter; `convert_one()` updated for H1-first order; `build_frontmatter()` updated for `title:` field.
- `tests/test_filename.py`: All path-based filename expectations must update.
- `tests/test_parse.py`, `tests/test_breadcrumbs.py`, `tests/test_toc.py`: Link resolution tests use new title-based filenames.
- No new dependencies.
