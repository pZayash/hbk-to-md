## Why

When multiple pages share the same H1 title (e.g. 22 pages titled "Ссылка (Ref)", 28 titled "Регистратор", 638 collisions total), `build_archive_index` maps all their archive paths to the same title-based filename. Link rewriting uses this index, so all links to colliding pages resolve to the first file — the disambiguation suffixes (`-2`, `-3`) are assigned at write time, after the index is already used, making them orphans with no inbound links.

## What Changes

- `build_archive_index` becomes two-pass: first scan all titles to detect duplicates, then resolve colliding pages via parent-page title enrichment
- For a colliding page, the converter walks up its archive path looking for a sibling `.html` file whose title serves as a prefix: `parent_title + "." + child_title → title_to_filename()`
- If no parent page is found, falls back to `archive_path_to_filename()` (existing behavior)
- `disambiguate()` remains as a safety net for any second-level collisions
- Existing `_collisions.log` continues to record cases that still needed disambiguation

## Capabilities

### New Capabilities

_(none — this change modifies an existing capability)_

### Modified Capabilities

- `title-based-filenames`: Collision resolution changes from opaque `-2`/`-3` suffixes to semantic parent-enriched names, and the `archive_index` is now guaranteed unique before link rewriting begins

## Impact

- `convert.py`: `build_archive_index()` — two-pass rewrite
- Vault output: existing colliding files (`Ссылка_(Ref)-2.md` … `-22.md`) replaced with semantic names; all inbound links corrected
- Tests: `test_filename.py` — collision scenario tests need updating
