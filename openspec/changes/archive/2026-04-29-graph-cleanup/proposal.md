## Why

Obsidian graph view for the generated vault is unreadable: a handful of nodes accumulate tens of thousands of edges (breadcrumb chains link every page to all ancestors; primitive-type pages attract 30 000+ incoming links), making the graph useless for navigation or exploration.

## What Changes

- **Breadcrumbs**: ancestor links converted to `obsidian://open?file=FILE` HTML anchors (not tracked by Obsidian graph engine); only the direct parent keeps a standard Markdown link `[title](file.md)`
- **Primitive type links**: MD links to built-in-type pages (`Строка`, `Число`, `Булево`, `Дата`, `Неопределено`, `Истина`, `Ложь`, `Null`) replaced with plain text — both in page body and in BSL signature blocks
- **Intermediate segment index pages removed**: `*__Свойства.md`, `*__Методы.md`, `*__События.md`, `*__Конструкторы.md`, `*__Поля.md`, `*__Параметры.md` etc. are no longer generated; segment nodes (`properties`, `methods`, `events`, `ctors`, `fields`, `params`, `formparams`) are skipped in index generation
- **Inline TOC removed**: the `<!-- toc:start/end -->` section injected on parent pages is no longer generated (it pointed to the now-removed segment index pages, and children are already listed in the page body)
- **`--breadcrumbs` CLI flag** added: `--breadcrumbs` (default off) controls whether breadcrumbs are injected at all; existing `--no-breadcrumbs` implied behavior becomes the new default

## Capabilities

### New Capabilities

- `graph-friendly-breadcrumbs`: Breadcrumb line uses HTML anchors for ancestors, single MD link for direct parent only — controls graph edge generation
- `primitive-type-suppression`: Configurable list of primitive-type filenames whose outgoing MD links are replaced with plain text at link-rewrite time and in BSL signature rendering
- `segment-index-suppression`: Segment-level intermediate index pages (`properties/`, `methods/`, etc.) are suppressed; their tree nodes are skipped in index generation and breadcrumb resolution

### Modified Capabilities

- `hbk-to-md-converter`: CLI gains `--breadcrumbs` flag (default: disabled); inline-TOC injection removed from post-processing pipeline

## Impact

- `convert.py`: `render_breadcrumb`, `build_index_name_map`, `write_all_indexes`, `inject_all_breadcrumbs`, `main` (new CLI arg)
- `signatures.py`: `render_type_tokens` — skip MD link when target is a primitive type
- Generated vault: `*__Свойства.md` / `*__Методы.md` / … files no longer produced; existing vaults need regeneration
- Tests: `test_breadcrumbs.py`, `test_toc.py` require updates
