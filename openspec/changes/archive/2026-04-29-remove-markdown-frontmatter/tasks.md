## 1. Remove frontmatter generation

- [x] 1.1 Update `convert.py` to stop generating content frontmatter (`build_frontmatter` / `convert_one` / `write_md` call flow).
- [x] 1.2 Update index rendering (`render_index`, `render_root_index`) to emit pure markdown without YAML blocks.
- [x] 1.3 Simplify breadcrumb insertion logic for the no-frontmatter layout (H1-first and no-H1 fallback).

## 2. Align tests with new markdown contract

- [x] 2.1 Replace/remove frontmatter-specific tests in `tests/test_parse.py` and add assertions for frontmatter absence.
- [x] 2.2 Update `tests/test_breadcrumbs.py` scenarios to validate insertion points without frontmatter.
- [x] 2.3 Extend `tests/test_toc.py` with checks that `_index.md` and `_index__*.md` do not start with `---`.

## 3. Update docs and validate behavior

- [x] 3.1 Update `README.md`: remove YAML-frontmatter section and refresh output examples for pure markdown format.
- [x] 3.2 Add a breaking-change note for downstream scripts that parse YAML from `.md`, with migration path to `_meta.json`.
- [x] 3.3 Run the test suite and verify generated sample vault files contain no frontmatter in any `.md`.
