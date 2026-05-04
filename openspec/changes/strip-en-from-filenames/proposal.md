## Why

The `title-based-filenames` spec already requires filenames to be derived from `title_ru` — the H1 text **before** the parenthesised English part. The current implementation passes the full raw H1 text (including `(English)`) to `title_to_filename`, which does not strip parentheses, producing filenames like `Булево_(Boolean).md` instead of the spec-correct `Булево.md`.

## What Changes

- `build_archive_index()`: strip the `(English)` parenthetical from H1 text before passing to `title_to_filename()`, using the existing `PAGETITLE_SPLIT_RE`
- `PRIMITIVE_TYPE_STEMS`: update hardcoded stems from `"lang__Булево_(Boolean)"` → `"lang__Булево"` etc. to match new filenames
- All generated `.md` filenames across both `shcntx` (objects) and `shlang` (built-in language) archives will drop the English suffix

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `title-based-filenames`: Implementation now correctly matches the existing spec requirement — filenames use `title_ru` only (no English parenthetical)
- `primitive-type-suppression`: Hardcoded stem set updated to match new filename format

## Impact

- All output `.md` filenames that previously included `_(EnglishName)` will change — existing Obsidian vaults built with old converter will have broken links until rebuilt
- Internal `v8help://` link rewriting unaffected — links resolve through `archive_index` which is also rebuilt with new names
- No CLI interface changes
- `PRIMITIVE_TYPE_STEMS` constant updated (affects `rewrite_links` logic for primitive type link suppression)
