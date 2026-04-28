## Why

Synthetic TOC index files have path-derived filenames (e.g., `_index__objects__catalog125__catalog126__CatalogsManager__methods.md`) that encode meaningless archive path segments (`catalog125`, `catalog126`) and sort far from the content pages they describe. In Obsidian and RAG pipelines, there is no way to identify which object an index belongs to without opening the file.

## What Changes

- Index files for section nodes (methods/properties/events/ctors) derive filenames from `node.title` of the nearest named ancestor + own section title (e.g., `СправочникиМенеджер_(CatalogsManager)__Методы.md`) — **BREAKING**: all existing `_index__*.md` filenames change except `_index.md` and first-level files.
- Level 0 (root) and level 1 (top-level: `objects`, `lang`) index files keep the `_index__` prefix for stable anchoring.
- Level 2+ index files drop the `_index__` prefix so they sort adjacent to their sibling content pages in the file explorer.
- A pre-computed `index_name_map: dict[str, str]` replaces the pure-function `index_filename_for(prefix)` call pattern, mirroring how `archive_index` works for content files.
- `parent_index:` frontmatter field in all index files updates to new filenames automatically.
- Vault must be regenerated with `--clean`.

## Capabilities

### New Capabilities

- `title-based-index-filenames`: Derive index file names from the tree node title chain (nearest named ancestor + section title) instead of the raw archive path; build a prefix→filename map before writing any index files.

### Modified Capabilities

- `hbk-to-md-converter`: Index filename derivation behavior changes (path-based → title-based); affects all callers of `index_filename_for()` and `parent_index_for()`.

## Impact

- `convert.py`: `index_filename_for()` and `parent_index_for()` replaced by `build_index_name_map()`; map threaded through `write_all_indexes()`, `render_index()`, `render_root_index()`, `resolve_breadcrumb_target()`.
- `tests/test_toc.py`: All index filename expectations must update.
- `tests/test_breadcrumbs.py`: `parent_index` references in breadcrumb tests must update.
- No new dependencies.
