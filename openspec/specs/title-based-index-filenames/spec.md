## Purpose

Define human-readable index filename derivation and map-based index linking.

## Requirements

### Requirement: Index name map built from node titles
The system SHALL compute a `prefix → filename` map for all index files once, after `propagate_titles()` resolves node titles, before any index files are written. The map SHALL be passed explicitly to all functions that generate or reference index filenames.

#### Scenario: Map built before writing
- **WHEN** `main()` calls `write_all_indexes()`
- **THEN** `build_index_name_map()` has already been called and its result is passed as an argument

#### Scenario: Map seeded with content filenames
- **WHEN** `build_index_name_map()` runs
- **THEN** the internal `used_names` set is pre-seeded with all values from `archive_index` so that index names cannot collide with content filenames

### Requirement: Level-based prefix rule
The system SHALL apply a prefix rule based on the depth of the node's prefix path:
- Depth 0 (root): filename is always `_index.md`
- Depth 1 (e.g., `objects`, `lang`): filename is `_index__<title_stem>.md`
- Depth 2+: filename has NO `_index__` prefix

#### Scenario: Root index unchanged
- **WHEN** deriving the filename for the root node (prefix = `""`)
- **THEN** filename is `_index.md`

#### Scenario: Top-level index keeps prefix
- **WHEN** deriving the filename for a depth-1 node (e.g., prefix = `"objects"`, title = "Объекты")
- **THEN** filename is `_index__Объекты.md`

#### Scenario: Section index has no prefix
- **WHEN** deriving the filename for a depth-5 section node (e.g., `.../CatalogsManager/methods`)
- **THEN** filename does NOT start with `_index__`

### Requirement: Section index names derived from nearest named ancestor
The system SHALL derive the stem for depth-2+ index files as `<ancestor_title>__<own_title>` where the ancestor is the nearest ancestor node satisfying all of:
1. `node.title != node.segment` (title was resolved, not raw fallback)
2. `node.segment not in SEGMENT_NAMES` (not a generic category node like "objects", "methods")

If no such ancestor exists, the stem is the node's own title.

#### Scenario: Section node with named object ancestor
- **WHEN** node is `objects/.../CatalogsManager/methods` with ancestor title "СправочникиМенеджер_(CatalogsManager)" and own title "Методы"
- **THEN** stem is `СправочникиМенеджер_(CatalogsManager)__Методы` and filename is `СправочникиМенеджер_(CatalogsManager)__Методы.md`

#### Scenario: Section node with no named ancestor
- **WHEN** node has no ancestor satisfying the named-ancestor criteria
- **THEN** stem is the node's own title and filename is `<title>.md`

#### Scenario: Node with raw segment title
- **WHEN** `node.title == node.segment` (e.g., title = "catalog2", segment = "catalog2")
- **THEN** system falls back to path-based filename (same as current `archive_path_to_filename()` behavior)

### Requirement: Filename length capped at 250 characters
The system SHALL truncate the stem to ensure the total filename (including extension) does not exceed 250 characters before passing to `disambiguate()`.

#### Scenario: Long title truncated
- **WHEN** the derived stem would produce a filename longer than 250 characters
- **THEN** the stem is truncated so the final filename is at most 250 characters

### Requirement: Index filenames are collision-free
The system SHALL pass every derived index filename through `disambiguate()` using the same `used_names` set, appending `-2`, `-3` suffixes as needed.

#### Scenario: Duplicate stems disambiguated
- **WHEN** two different nodes produce the same derived stem
- **THEN** the second filename gets a `-2` suffix (e.g., `Объект__Свойства-2.md`)

### Requirement: All internal index references use the map
The system SHALL use `index_name_map` lookups (not `index_filename_for()`) for all internal references: `parent_index` frontmatter, child links in index bodies, and breadcrumb link resolution in content files.

#### Scenario: Parent index frontmatter correct
- **WHEN** a section index file is written
- **THEN** its `parent_index:` frontmatter field contains the new title-based filename of its parent node

#### Scenario: Breadcrumb in content file resolves correctly
- **WHEN** `resolve_breadcrumb_target()` resolves the parent index for a content page
- **THEN** it looks up the parent prefix in `index_name_map` and uses the resulting title-based filename
