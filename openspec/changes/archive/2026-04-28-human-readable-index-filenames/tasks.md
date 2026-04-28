## 1. Build index name map

- [x] 1.1 Add `SEGMENT_NAMES = set(SEGMENT_TITLES.keys())` constant
- [x] 1.2 Implement `stem_for(node: TreeNode, prefix_map: dict[str, TreeNode]) -> str` — walk ancestors to find nearest named non-segment ancestor; return `ancestor.title + "__" + node.title` or `node.title` alone; return `""` for raw-fallback nodes
- [x] 1.3 Implement `build_index_name_map(root: TreeNode, prefix_map: dict[str, TreeNode], archive_index: dict[str, str]) -> dict[str, str]` — walk all nodes, apply level-based prefix rule (depth 0/1 keep `_index__`, depth 2+ drop it), call `title_to_filename()` for the stem, truncate to 246 chars before `.md`, run through `disambiguate()` with `used_names` seeded from `archive_index.values()`

## 2. Wire map into pipeline

- [x] 2.1 In `main()`, call `build_index_name_map(tree, prefix_map, archive_index)` after `propagate_titles()`, before `write_all_indexes()`
- [x] 2.2 Update `write_all_indexes(tree, out_dir, archive_index, index_name_map)` — replace `index_filename_for(node.prefix)` with `index_name_map[node.prefix]`; replace `parent_index_for(node.prefix)` with `index_name_map.get(parent_prefix)`
- [x] 2.3 Update `render_index(node, parent_index, archive_index, index_name_map, prefix_map)` — replace `index_filename_for(c.prefix)` child links with `index_name_map.get(c.prefix)`
- [x] 2.4 Update `render_root_index()` — replace `index_filename_for(child.prefix)` with `index_name_map.get(child.prefix)`
- [x] 2.5 Update `resolve_breadcrumb_target(prefix, archive_index, index_name_map, prefix_map)` — replace `index_filename_for(prefix)` with `index_name_map.get(prefix)`

## 3. Remove deprecated helpers

- [x] 3.1 Remove `parent_index_for(prefix)` — replaced by direct map lookup in callers
- [x] 3.2 Keep `index_filename_for(prefix)` only as internal fallback inside `build_index_name_map()` for raw-segment nodes; mark it private or remove if no longer needed externally

## 4. Tests — update expectations

- [x] 4.1 Update `tests/test_toc.py` — replace all path-based `_index__` filename expectations with title-based names; add test for `stem_for()` with named ancestor; add test for raw-segment fallback; add test for depth-1 prefix rule
- [x] 4.2 Update `tests/test_breadcrumbs.py` — replace `parent_index` references that used old path-based names

## 5. Verify end-to-end

- [x] 5.1 Run `pytest` — all tests pass
- [x] 5.2 Run full conversion on real `.hbk` with `--clean`; spot-check 10 index files: confirm title-based filename, correct `parent_index:` field, correct child links
- [x] 5.3 Verify sort order in vault directory: section index files appear adjacent to their parent content files
- [x] 5.4 Open vault in Obsidian — confirm file explorer shows readable index names grouped near object pages
