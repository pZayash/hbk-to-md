## 1. Core Implementation

- [x] 1.1 Add `resolve_parent_title(rel_path, title_map) -> str` function that walks up path trying `<parent_dir>.html` sibling lookups in `title_map`
- [x] 1.2 Rewrite `build_archive_index` as two-pass: Pass 1 collects `(rel, title)` pairs and counts title occurrences via `Counter`; Pass 2 assigns filenames — unique titles use `title_to_filename`, colliding titles use `resolve_parent_title` enrichment or `archive_path_to_filename` fallback
- [x] 1.3 Guard the two-pass logic behind `title_map is not None` so shlang archive (`title_map=None`) keeps existing single-pass behavior

## 2. Tests

- [x] 2.1 Update existing collision scenario in `test_filename.py`: colliding pages now get parent-enriched names, not `-2` suffixes
- [x] 2.2 Add scenario: colliding page with no ancestor HTML falls back to `archive_path_to_filename`
- [x] 2.3 Add scenario: `archive_index` returned by `build_archive_index` has all-unique values when titles collide
- [x] 2.4 Add scenario: non-colliding pages are unaffected by two-pass logic
- [x] 2.5 Add scenario: `title_map=None` skips enrichment (single-pass path unchanged)

## 3. Validation

- [x] 3.1 Run full conversion against `shcntx_ru.hbk` 8.3.27.1786; verify no files named `Ссылка_(Ref)-2.md` … `-22.md` exist in output
- [x] 3.2 Verify `_meta.json` collisions count is ≤ original 638 (ideally near zero for the known top-collision titles)
- [x] 3.3 Spot-check 3–5 previously colliding pages (e.g. Ссылка, Регистратор, Период) — confirm inbound links in other vault files resolve correctly
- [x] 3.4 Run test suite (`pytest`) — all tests pass
