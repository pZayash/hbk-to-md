## 1. Pass 0 — Title pre-scan

- [x] 1.1 Add `_H1_RE` regex constant for `<h1 class="V8SH_pagetitle">` extraction (no BeautifulSoup)
- [x] 1.2 Implement `quick_extract_title(path: Path) -> str` — reads first 4096 bytes, applies `_H1_RE`, strips inner HTML tags, returns raw text or `""`
- [x] 1.3 Implement `quick_scan_titles(extracted_dir: Path) -> dict[str, str]` — iterates `iter_html(extracted_dir)`, calls `quick_extract_title`, keys are `rel_path.lower()`

## 2. Title-to-filename derivation

- [x] 2.1 Add `_UNSAFE_CHARS` regex constant (`[/\\:*?"<>|]`)
- [x] 2.2 Implement `title_to_filename(title: str, prefix: str = "") -> str` — strips unsafe chars, replaces spaces with `_`, strips leading/trailing `._`, prepends prefix, appends `.md`; returns `""` if result is empty
- [x] 2.3 Update `build_archive_index(extracted_dir, prefix, title_map=None)` — when `title_map` provided, use `title_to_filename(title_map.get(rel.lower(), ""), prefix)` as target; fall back to `archive_path_to_filename()` when result is empty

## 3. Wire Pass 0 into main pipeline

- [x] 3.1 In `main()`, call `quick_scan_titles(ctx_dir)` after `extract_hbk(args.hbk, ctx_dir)`, before `build_archive_index(ctx_dir, prefix="")`
- [x] 3.2 Pass title_map into `build_archive_index()` for shcntx
- [x] 3.3 If `args.lang_hbk`: call `quick_scan_titles(lang_dir)` after extraction; pass title_map into `build_archive_index()` for shlang
- [x] 3.4 Verify `archive_lookup_final` still populated correctly in `convert_one()` for both title-based and path-based fallback names

## 4. Frontmatter — restore title: field

- [x] 4.1 Update `build_frontmatter(meta: dict) -> str` — render only `title` field (from `meta["title_ru"] or meta["title_en"]`); skip if empty; skip all other fields
- [x] 4.2 Update `convert_one()` — pass `fm = {"title_ru": title_ru, "title_en": title_en}` to `build_frontmatter()`; use returned string as frontmatter arg to `write_md()`

## 5. Content order — H1 before breadcrumb

- [x] 5.1 Update `inject_breadcrumb_into_content()` — detect first `# ` heading line; insert breadcrumb AFTER it (+ blank line), not before; handle edge case of no H1 (insert at top as before)
- [x] 5.2 Update the no-frontmatter branch in `inject_breadcrumb_into_content()` to check for leading `# ` before deciding insertion point

## 6. Tests — update expectations

- [x] 6.1 Update `tests/test_filename.py` — replace path-based filename expectations with title-based; add test for `title_to_filename()` sanitization; add test for empty-title fallback
- [x] 6.2 Update `tests/test_parse.py` — update any fixture that checks output filenames
- [x] 6.3 Update `tests/test_breadcrumbs.py` — verify breadcrumb appears AFTER H1, not before
- [x] 6.4 Update `tests/test_toc.py` — update link targets in index expectations to use title-based names

## 7. Verify end-to-end

- [x] 7.1 Run `pytest` — all tests pass
- [x] 7.2 Run full conversion on real `.hbk` with `--clean`; spot-check 10 output files: confirm title-based filename, frontmatter `title:`, H1 as first line, breadcrumb below H1
- [x] 7.3 Verify `_meta.json` `converted` count matches previous run (no pages lost to empty-title fallback beyond expected)
- [x] 7.4 Open vault in Obsidian — confirm file explorer shows readable names; quick-switcher search by Russian term finds correct page
