## MODIFIED Requirements

### Requirement: Collision between two pages with same title

When multiple pages produce the same title-based filename, the converter SHALL resolve the collision by enriching the filename with the nearest ancestor page's title rather than appending a numeric suffix.

The collision resolution algorithm is:

1. **Detection pass (Pass 0.5)**: after `quick_scan_titles()` runs, count title occurrences. Any title appearing more than once is a *colliding title*.
2. **Parent lookup**: for a page at `a/b/c/file.html` whose title is colliding, walk up the path trying `a/b/c.html`, then `a/b.html`, then `a.html` — using `title_map.get(candidate.lower())`. Use the first non-empty title found.
3. **Enriched filename**: call `title_to_filename(parent_title + "." + child_title)`. The resulting name follows the existing `Родитель.Дочерний_(Parent.Child).md` convention.
4. **Fallback**: if no ancestor page title is found, use `archive_path_to_filename(rel_path)`.
5. **Safety net**: `disambiguate()` continues to be applied in `convert_one` for any second-level collisions that survive enrichment.

The `archive_index` built by `build_archive_index` SHALL be unique (no two `rel_path` keys map to the same filename value) before `rewrite_links` is called.

#### Scenario: Colliding pages get parent-enriched filenames

- **WHEN** `tables/table6/fields/Ref38.html` and `tables/table81/fields/Ref645.html` both have title `"Ссылка (Ref)"`
- **AND** `title_map` contains `"tables/table6.html" → "Каталог.<Имя справочника> (Catalog.<Имя справочника>)"`
- **AND** `title_map` contains `"tables/table81.html" → "ВнешнийИсточникДанных...<Имя> (ExternalDataSource...<Name>)"`
- **THEN** `archive_index["tables/table6/fields/ref38.html"]` = `"Каталог.Имя_справочника_(Catalog.Имя_справочника).Ссылка_(Ref).md"`
- **THEN** `archive_index["tables/table81/fields/ref645.html"]` starts with `"ВнешнийИсточникДанных"` and ends with `".Ссылка_(Ref).md"` (possibly truncated)
- **THEN** both values are distinct

#### Scenario: Archive index is unique before link rewriting

- **WHEN** `build_archive_index()` is called on a directory containing pages with duplicate titles
- **THEN** no two distinct `rel_path` keys in the returned dict share the same filename value

#### Scenario: Non-colliding pages are unaffected

- **WHEN** a page has a title that appears exactly once across the archive
- **THEN** its filename is derived by `title_to_filename(title)` as before — no parent lookup is performed

#### Scenario: Colliding page with no ancestor HTML falls back to path-based name

- **WHEN** a page has a colliding title
- **AND** no ancestor directory has a sibling `.html` file in `title_map`
- **THEN** the filename is `archive_path_to_filename(rel_path)` — path segments joined with `__`

#### Scenario: Second-level collision still gets disambiguated

- **WHEN** two colliding pages share both the same title and the same ancestor page title
- **THEN** the second page receives a `-2` suffix via `disambiguate()`
- **THEN** the collision is logged to `_collisions.log`

#### Scenario: title_map=None skips enrichment (shlang archive)

- **WHEN** `build_archive_index()` is called with `title_map=None`
- **THEN** collision detection is skipped
- **THEN** all pages use `title_to_filename(title)` if title is available, else `archive_path_to_filename()`
- **THEN** any remaining collisions are resolved by `disambiguate()` as before
