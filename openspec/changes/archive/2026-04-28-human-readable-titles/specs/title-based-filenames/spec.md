## ADDED Requirements

### Requirement: Pre-scan pass extracts titles before archive index is built

Before building `archive_index`, the converter SHALL perform a lightweight title-extraction pass (Pass 0) over all HTML files in the extracted directory. Pass 0 SHALL read only the first 4096 bytes of each file, extract the text content of `<h1 class="V8SH_pagetitle">` via regex (no full parse), and return a `dict[str, str]` mapping `rel_path.lower() → raw_h1_text`. Pages with no matching H1 SHALL map to empty string.

#### Scenario: Pass 0 extracts H1 from shcntx page

- **WHEN** `quick_scan_titles()` is called on a directory containing `objects/Global context/methods/catalog1566/CanReadXML1628.html` whose `<h1 class="V8SH_pagetitle">` contains `Глобальный контекст.ВозможностьЧтенияXML (Global context.CanReadXML)`
- **THEN** the returned dict contains key `objects/global context/methods/catalog1566/canreadxml1628.html` with value `Глобальный контекст.ВозможностьЧтенияXML (Global context.CanReadXML)`

#### Scenario: Pass 0 handles page with no H1

- **WHEN** `quick_scan_titles()` processes an HTML file with no `<h1 class="V8SH_pagetitle">` element
- **THEN** the returned dict contains that file's key with value `""` (empty string)

#### Scenario: Pass 0 handles extensionless shlang files

- **WHEN** `quick_scan_titles()` processes shlang files without `.html` extension (e.g., `def_String`)
- **THEN** those files are included in the scan results using the same key format as `iter_html()` produces

### Requirement: Title-based filename derivation

The converter SHALL derive `.md` filenames from the page's `title_ru` (the full H1 text before the parenthesised part) rather than from the archive path. The derivation SHALL:
1. Strip characters unsafe for filenames: `/\:*?"<>|`
2. Replace space characters with `_`
3. Strip leading/trailing `.` and `_`
4. Prepend archive prefix (e.g., `lang__`) if applicable
5. Append `.md`

If the sanitized result is empty (no safe characters remain), the converter SHALL fall back to path-based filename derivation via `archive_path_to_filename()`.

#### Scenario: Method page gets title-based filename

- **WHEN** HTML page has `<h1 class="V8SH_pagetitle">Глобальный контекст.ВозможностьЧтенияXML (Global context.CanReadXML)</h1>`
- **THEN** `title_ru` = `"Глобальный контекст.ВозможностьЧтенияXML"`
- **THEN** the output filename is `Глобальный_контекст.ВозможностьЧтенияXML.md`

#### Scenario: Simple title page gets title-based filename

- **WHEN** HTML page has `<h1 class="V8SH_pagetitle">Глобальный контекст</h1>` (no parenthesised part)
- **THEN** the output filename is `Глобальный_контекст.md`

#### Scenario: shlang page keeps archive prefix

- **WHEN** a page from `shlang_ru.hbk` has title `"Строка"` and prefix `lang__`
- **THEN** the output filename is `lang__Строка.md`

#### Scenario: Page with no extractable title falls back to path-based name

- **WHEN** a page has no `<h1 class="V8SH_pagetitle">` element
- **THEN** the output filename is the path-derived name (same as current behavior via `archive_path_to_filename()`)

#### Scenario: Collision between two pages with same title

- **WHEN** two pages in the same conversion run both produce `Найти.md` after sanitization
- **THEN** the second page receives filename `Найти-2.md` (via existing `disambiguate()`)
- **THEN** the collision is logged to `_collisions.log`

### Requirement: archive_index uses title-based filenames for link resolution

The `archive_index` (used for `v8help://` link resolution) SHALL map `rel_path.lower()` to the title-based filename (not the path-based name). This ensures internal links within converted pages point to the correct title-named output files.

#### Scenario: v8help link resolves to title-based filename

- **WHEN** a page contains `<a href="v8help://SyntaxHelperContext/objects/Global context/methods/catalog1566/CanReadXML1628.html">`
- **THEN** the rewritten Markdown link targets `Глобальный_контекст.ВозможностьЧтенияXML.md`
- **THEN** that file exists in the output directory
