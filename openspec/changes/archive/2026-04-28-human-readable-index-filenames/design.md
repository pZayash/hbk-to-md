## Context

`convert.py` generates synthetic TOC index files for every tree node that has children but no content page. Currently `index_filename_for(prefix: str) -> str` is a pure deterministic function that encodes the full archive path as double-underscore-separated segments. This embeds meaningless intermediate path components (`catalog125`, `catalog126`, `object128`) into filenames.

By the time `write_all_indexes()` is called, `propagate_titles()` has already resolved `node.title` for every node from `pages_meta` (title_ru) or `SEGMENT_TITLES`. The data for human-readable naming is available — it is simply not used.

Index files only exist for nodes where: prefix ≠ `""` AND `node.children` is non-empty AND `node.content_filename` is None. Intermediate `catalogNN` grouping nodes always have content pages (the category overview page), so they are already excluded from index generation. The generated index files are exclusively section-level nodes: `methods`, `properties`, `events`, `ctors`, and rare cases at other depths.

Primary consumers: Obsidian file explorer (sort order, quick-switcher) and a RAG pipeline (chunk metadata, filename as document identifier).

## Goals / Non-Goals

**Goals:**
- Index filenames for section nodes derive from nearest named ancestor title + own section title
- Level 0 (`_index.md`) and level 1 (`_index__Объекты.md`, `_index__Встроенный_язык.md`) keep `_index__` prefix for stable navigation anchors
- Level 2+ index files have no `_index__` prefix — sort adjacent to sibling content pages
- All internal references (parent_index frontmatter, breadcrumb links, child links in parent index) update automatically via the map
- Filename length capped at 250 characters; collision handling via existing `disambiguate()`

**Non-Goals:**
- Changing `_index.md` (root) or first-level index names beyond title-based derivation
- Changing content file naming (handled by `human-readable-titles` change)
- Index files for intermediate catalog grouping nodes (already excluded by existing logic)
- English transliteration; Cyrillic filenames are acceptable on all target systems

## Decisions

### 1. Replace `index_filename_for()` with `build_index_name_map()`

Add `build_index_name_map(root, prefix_map) -> dict[str, str]` that walks the tree once after `propagate_titles()` and returns `prefix → filename`. All callers that currently call `index_filename_for(prefix)` look up from this map instead.

```
build_hierarchy() + propagate_titles()
  ↓
build_index_name_map(root, prefix_map)   ← new, one-time pass
  ↓
write_all_indexes(tree, out_dir, archive_index, index_name_map)
render_index(..., index_name_map)
resolve_breadcrumb_target(..., index_name_map)
```

**Alternative considered**: patch `index_filename_for()` to accept an optional title map parameter. Rejected — partial patching leaves pure-function callers inconsistent and requires threading state anyway.

**Alternative considered**: post-rename pass (generate with old names, rename, rewrite references). Rejected — O(n) file renames + O(n) reference rewrites across all markdown files, high fragility.

### 2. `stem_for(node)` — title chain derivation

```python
SEGMENT_NAMES = set(SEGMENT_TITLES.keys())
# {"methods","properties","events","ctors","objects","tables","lang","Global context"}

def stem_for(node: TreeNode, prefix_map: dict[str, TreeNode]) -> str:
    if not node.title or node.title == node.segment:
        return ""  # raw fallback → path-based name

    parts = [p for p in node.prefix.split("/") if p]
    for i in range(len(parts) - 1, 0, -1):
        ancestor = prefix_map.get("/".join(parts[:i]))
        if (ancestor
                and ancestor.title
                and ancestor.title != ancestor.segment
                and ancestor.segment not in SEGMENT_NAMES):
            return ancestor.title + "__" + node.title

    return node.title  # no qualifying ancestor → use own title
```

**Why skip SEGMENT_NAMES ancestors?** Nodes like `objects` (title "Объекты") are too generic to serve as distinguishing prefix. Object nodes (e.g., `CatalogsManager`, title "СправочникиМенеджер_(CatalogsManager)") are specific and unique — they are the right prefix for section names.

**Alternative considered**: use full title path from root. Rejected — produces filenames like `Объекты__Прикладные_объекты__Справочники__СправочникиМенеджер__Методы.md` which are long and still contain generic category names.

### 3. Level-based prefix rule

```python
depth = len([p for p in node.prefix.split("/") if p])

if depth == 0:
    filename = "_index.md"
elif depth == 1:
    filename = f"_index__{title_to_filename(node.title, prefix='')}"
else:
    stem = stem_for(node, prefix_map)
    if stem:
        filename = title_to_filename(stem, prefix="")[:246] + ".md"
    else:
        filename = archive_path_to_filename(node.prefix)  # path-based fallback
```

**Why two levels with `_index__`?** Root and top-level nodes (`objects`, `lang`) are global navigation anchors. They are stable, known entry points referenced from README and external notes. Keeping `_index__` prefix makes them visually distinct and prevents sort-order interference with content files (there are no content files named "Объекты.md" or "Встроенный_язык.md" without qualifiers at the vault root).

### 4. Disambiguation via existing `disambiguate()`

`build_index_name_map()` maintains a `used_names: set[str]` seeded with `{"_index.md"}`. Each derived filename passes through `disambiguate(name, used_names)` before insertion. The `used_names` set must also include all content filenames to prevent collision between an index file and a content file with the same derived stem.

### 5. `title_to_filename()` reuse

The existing `title_to_filename(title, prefix)` function from the `human-readable-titles` change handles unsafe char stripping, space→`_` conversion, and `.md` suffix. Index derivation reuses it without modification. The `prefix` parameter is left empty — there is no `lang__` disambiguation needed for index files since section names are always qualified by their parent object name.

## Risks / Trade-offs

- **BREAKING** — All `_index__*.md` filenames except `_index.md` and `_index__Объекты.md`-style level-1 files change. External notes linking to old names break. **Mitigation**: vault always regenerated from source with `--clean`; document in README.

- **`parent_index:` frontmatter stale references** — If `build_index_name_map()` is called before `write_all_indexes()` and both use the same map, references are always consistent. Order dependency must be enforced in `main()`. **Mitigation**: map is built once and passed explicitly; no global state.

- **`used_names` must include content filenames** — Without seeding content filenames into `used_names`, a section index could get the same name as an existing content file. **Mitigation**: seed `used_names` from `archive_index.values()` before the index name derivation walk.

- **Cyrillic filenames** — Same risk as `human-readable-titles` change. Acceptable for target platforms.

## Migration Plan

Not applicable — tool generates vault fresh from `.hbk` on each run. Regenerate with `--clean`; existing vault replaced entirely.
