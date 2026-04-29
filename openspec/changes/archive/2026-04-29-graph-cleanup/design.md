## Context

Converter produces ~29 000 Markdown files. Post-processing injects breadcrumbs (full ancestor chain as MD links) and inline TOC sections. Three hub patterns make the Obsidian graph unreadable:

1. Every page links to `_index.md` (29 062 incoming), `_index__Объекты.md` (28 209), etc. via breadcrumb MD links.
2. Primitive-type pages (`lang__def_String.md` etc.) accumulate 6 000–15 000 incoming links from type signatures.
3. Segment index pages (`*__Свойства.md`) add an extra navigation layer not present in the source hierarchy.

Obsidian graph engine tracks `[text](file.md)` and `[[wikilinks]]` but ignores raw HTML `<a href>` tags. This is the key leverage point.

## Goals / Non-Goals

**Goals:**
- Reduce graph edge count dramatically without losing navigation (breadcrumb still visible and clickable)
- Remove intermediate segment index pages that add noise without unique content
- Remove inline TOC that duplicates body content
- Add `--breadcrumbs` flag (default off) so users can opt in to full breadcrumb injection

**Non-Goals:**
- YAML frontmatter / `hbk_type` metadata (deferred)
- `.obsidian/graph.json` generation (deferred)
- Changing page content or link text in any way visible to the reader

## Decisions

### D1: HTML anchor format for non-parent breadcrumb links

**Decision**: Use `<a href="obsidian://open?file=FILENAME">title</a>` for all breadcrumb ancestors except the direct parent. Direct parent stays `[title](filename)`.

**Alternatives considered**:
- Drop ancestors entirely — loses navigability for humans
- Keep full MD breadcrumb but add `--no-graph-breadcrumbs` flag — still pollutes graph when breadcrumbs on
- Use `obsidian://open?vault=NAME&file=FILE` — requires vault name as CLI arg; user verified `?file=` alone works

**Rationale**: Best of both worlds — full visual breadcrumb, single graph edge to direct parent.

### D2: Primitive type suppression via filename prefix/set match

**Decision**: Define `PRIMITIVE_TYPE_STEMS` — a set of `lang__def_*` stems and known primitive-type filenames. In `rewrite_links`, when resolved `target_filename` matches, emit plain text (link text only, no anchor). In `render_type_tokens` (signatures.py), same check: emit `` `Name` `` without a link.

**Alternatives considered**:
- HTML anchor for primitives — keeps them clickable but adds complexity; user decided plain text is sufficient
- Runtime flag `--no-primitive-links` — adds CLI surface; simpler to hardcode the set since primitives are stable

**Rationale**: Primitives are universal knowledge; 34 000 edges eliminated with a small constant set.

The set includes:
```
lang__def_String, lang__def_Number, lang__def_Date,
lang__def_Undefined, lang__def_BooleanTrue, lang__def_BooleanFalse, lang__def_Null,
lang__Булево_(Boolean), lang__Число_(Number), lang__Строка_(String),
lang__Дата_(Date), lang__Неопределено_(Undefined)
```
(matched by stem, i.e. filename without `.md`)

### D3: Segment index suppression via skip set

**Decision**: Add `SKIP_SEGMENT_INDEX: set[str]` = `{"properties", "methods", "events", "ctors", "fields", "params", "formparams"}`. In `build_index_name_map` and `write_all_indexes`, skip `TreeNode` entries where `node.segment in SKIP_SEGMENT_INDEX`. These nodes remain in the tree (for hierarchy traversal) but produce no `.md` file and no entry in `index_name_map`.

**Effect on breadcrumbs**: `resolve_breadcrumb_target` looks up `index_name_map`; missing entry → returns `None` → `render_breadcrumb` skips the segment → direct parent becomes the class page itself.

**Effect on content pages**: Class pages' bodies already list child links (from original HTML). The segment level disappears from navigation silently.

### D4: Inline TOC removal

**Decision**: Remove the `inject_inline_toc_into_content` call from `inject_all_breadcrumbs`. The TOC pointed to segment index pages (now removed). Class page bodies already carry child links from the source HTML.

**Alternative**: Keep TOC but rewrite it to point directly to children — more work, same outcome since body already has the links.

### D5: `--breadcrumbs` flag (default off)

**Decision**: Add `--breadcrumbs` boolean flag. When absent (default), skip the entire `STAGE_INJECT_BREADCRUMBS` stage. Existing behaviour (breadcrumbs on) requires explicit `--breadcrumbs`.

**Rationale**: Most useful for agent/AI consumers who don't need visual navigation. Human users who want navigation opt in.

## Risks / Trade-offs

- **Existing vaults break**: `*__Свойства.md` files referenced by old pages won't be regenerated. Mitigation: document that `--clean` regeneration is required.
- **obsidian:// URL portability**: `obsidian://open?file=` works in the user's tested setup but may require `?vault=` in some configurations. Mitigation: document limitation; add `--vault-name` flag later if needed.
- **Primitive set completeness**: New platform versions may introduce new primitive pages not in the hardcoded set. Mitigation: use `lang__def_` prefix pattern as fallback rule.
- **Test coverage**: `test_breadcrumbs.py` and `test_toc.py` test current behaviour; they will fail and need updating. Mitigation: update tests as part of this change.

## Migration Plan

1. Regenerate vault with `--clean --breadcrumbs` (or without `--breadcrumbs` for graph-optimised output)
2. No incremental migration path — full regeneration required
3. Rollback: revert to previous binary, regenerate
