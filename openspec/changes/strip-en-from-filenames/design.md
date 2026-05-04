## Context

`title_to_filename(title)` receives a raw H1 string such as `"Булево (Boolean)"`. The regex `_UNSAFE_CHARS = re.compile(r'[/\\:*?"<>|]')` does **not** strip parentheses, so spaces become `_` and the result is `"Булево_(Boolean).md"`.

`PAGETITLE_SPLIT_RE = re.compile(r"^(.*)\s*\(([^()]*)\)\s*$")` already exists and correctly extracts `group(1)` (Russian) and `group(2)` (English). It is used in `extract_titles()` but not in the filename-generation path.

`PRIMITIVE_TYPE_STEMS` is a hardcoded `frozenset` used in `rewrite_links()` to suppress links to primitive types. Its stems contain the old `_(Boolean)` form.

## Goals / Non-Goals

**Goals:**
- Output filenames contain only the Russian part of the H1 title
- Both `shcntx` and `shlang` archives affected uniformly
- `PRIMITIVE_TYPE_STEMS` stays consistent with generated filenames
- No CLI changes, no new dependencies

**Non-Goals:**
- English-language filename mode (not needed — separate EN hbk files exist)
- Migrating existing vaults (users must re-run the converter)

## Decisions

### Decision: Apply stripping inside `build_archive_index`, not in `title_to_filename`

`title_to_filename` is a pure sanitizer — it should not know about domain-specific title structure. The split belongs one level up, where `title_map` values are consumed.

**Alternative considered:** patch `title_to_filename` to apply `PAGETITLE_SPLIT_RE` internally. Rejected: the function is generic and callers may legitimately pass titles without the `(English)` pattern.

**Implementation:**
```python
# in build_archive_index(), before calling title_to_filename:
m = PAGETITLE_SPLIT_RE.match(title)
ru_title = m.group(1).strip() if m else title
target = title_to_filename(ru_title, prefix=prefix)
```

### Decision: Update `PRIMITIVE_TYPE_STEMS` statically

The stems in `PRIMITIVE_TYPE_STEMS` are a closed, known set that maps 1-to-1 to the new Russian-only filenames. Update them inline — no dynamic computation needed.

Old → New:
- `"lang__Булево_(Boolean)"` → `"lang__Булево"`
- `"lang__Число_(Number)"` → `"lang__Число"`
- `"lang__Строка_(String)"` → `"lang__Строка"`
- `"lang__Дата_(Date)"` → `"lang__Дата"`
- `"lang__Неопределено_(Undefined)"` → `"lang__Неопределено"`

The `lang__def_*` stems are path-derived (no title), so they are unchanged.

## Risks / Trade-offs

- **Breaking change for existing vaults** → Mitigation: document in changelog; users re-run converter to rebuild. No partial migration path needed.
- **`PAGETITLE_SPLIT_RE` false positives** — a title ending in `(something)` that is not actually an English name (e.g., a note in parentheses). → Low risk: 1C help titles follow this pattern consistently. The regex requires the match to span the full title (`^...$`), limiting false matches.
- **Pages with no English part** — `PAGETITLE_SPLIT_RE` will not match; `title` used as-is. No regression. ✓
