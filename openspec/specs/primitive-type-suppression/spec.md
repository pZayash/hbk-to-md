## Purpose

Define suppression of hyperlinks to primitive BSL type pages to reduce Obsidian graph noise from high-degree type nodes.

## Requirements

### Requirement: Links to primitive-type pages are suppressed

The converter SHALL maintain a set `PRIMITIVE_TYPE_STEMS` of known primitive-type page stems. When `rewrite_links` resolves a link whose `target_filename` stem is in this set, it SHALL emit plain text (the link's visible text) rather than a Markdown link. In BSL signature rendering (`render_type_tokens`), tokens whose link target stem is in the set SHALL be rendered as `` `Name` `` without a hyperlink.

The set SHALL include at minimum:

- `lang__def_String`, `lang__def_Number`, `lang__def_Date`
- `lang__def_Undefined`, `lang__def_BooleanTrue`, `lang__def_BooleanFalse`, `lang__def_Null`
- `lang__Булево_(Boolean)`, `lang__Число_(Number)`, `lang__Строка_(String)`
- `lang__Дата_(Date)`, `lang__Неопределено_(Undefined)`

Matching SHALL be case-insensitive and applied to the stem (filename without `.md`).

#### Scenario: Строка type link in property description becomes plain text

- **WHEN** an HTML page contains `<a href="v8help://...def_String">Строка</a>`
- **THEN** the converted Markdown contains the plain text `Строка` with no surrounding `[...](...)`
- **THEN** Obsidian graph shows no edge from this page to `lang__def_String.md`

#### Scenario: BSL signature with Булево type has no link

- **WHEN** signatures.py renders a property type of `Булево`
- **THEN** the signature line reads `` `PropertyName`: `Булево` `` (no hyperlink)

#### Scenario: Non-primitive type link is preserved

- **WHEN** an HTML page contains a link to a non-primitive class like `ГруппаВыбранныхПолей`
- **THEN** the converted Markdown preserves the full `[ГруппаВыбранныхПолей](filename.md)` link
