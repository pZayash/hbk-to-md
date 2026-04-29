## ADDED Requirements

### Requirement: Breadcrumb ancestors use HTML anchors to avoid graph edges

When breadcrumbs are enabled, all ancestor links except the direct parent SHALL be rendered as raw HTML `<a href="obsidian://open?file=FILENAME">title</a>` anchors. The direct parent SHALL be rendered as a standard Markdown link `[title](filename)`. The home link (Главная / `_index.md`) is treated as an ancestor and also rendered as an HTML anchor.

This exploits the fact that Obsidian's graph engine does not parse raw HTML `<a href>` tags, so only one graph edge (to the direct parent) is created per page.

#### Scenario: Property page breadcrumb has one MD link

- **WHEN** a property page at depth 6 has breadcrumbs injected
- **THEN** exactly one standard Markdown link `[title](file.md)` appears in the breadcrumb line (the direct parent)
- **THEN** all other ancestors appear as `<a href="obsidian://open?file=...">` HTML anchors
- **THEN** Obsidian graph shows exactly one edge from this property page to its parent

#### Scenario: Top-level page breadcrumb (depth 1) has one MD link

- **WHEN** a page whose direct parent is `_index.md` has breadcrumbs injected
- **THEN** the breadcrumb renders the direct parent (`_index.md`) as `[Главная](_index.md)` Markdown link
- **THEN** no HTML anchor is emitted (no ancestors above home)

#### Scenario: Breadcrumbs disabled by default

- **WHEN** converter is run without `--breadcrumbs` flag
- **THEN** no breadcrumb line is injected into any page
- **THEN** `STAGE_INJECT_BREADCRUMBS` is skipped entirely

#### Scenario: Breadcrumbs enabled via flag

- **WHEN** converter is run with `--breadcrumbs` flag
- **THEN** breadcrumb line is injected into all content pages with the HTML-anchor format
