## Purpose

Define suppression of intermediate index pages for structural segment nodes (properties, methods, events, etc.) that add graph noise without unique content.

## Requirements

### Requirement: Segment-level intermediate index pages are not generated

The converter SHALL define `SKIP_SEGMENT_INDEX` — a set of archive path segment names that act as grouping containers with no unique content. Nodes in the tree hierarchy whose `segment` is in this set SHALL be skipped during index page generation and SHALL NOT appear as breadcrumb stops.

`SKIP_SEGMENT_INDEX` SHALL contain: `properties`, `methods`, `events`, `ctors`, `fields`, `params`, `formparams`.

Skipping means:

- No `*__Свойства.md`, `*__Методы.md`, `*__События.md`, `*__Конструкторы.md`, etc. files are written to disk
- No entry for these nodes is added to `index_name_map`
- `render_breadcrumb` naturally skips them (no resolved target → skipped)
- The direct parent of a property/method page becomes the class page itself

These nodes remain in the `TreeNode` tree for hierarchy traversal but produce no output.

#### Scenario: No __Свойства.md files in output

- **WHEN** converter processes a class with a `properties/` directory
- **THEN** no file matching `*__Свойства.md` is created in the output directory
- **THEN** no file matching `*__Методы.md`, `*__События.md`, `*__Конструкторы.md` is created

#### Scenario: Property page breadcrumb skips segment level

- **WHEN** a property page with source path `objects/Foo/properties/Bar.html` has breadcrumbs enabled
- **THEN** the breadcrumb chain goes `Главная › ... › Foo` (the class), NOT `Главная › ... › Foo › Свойства`
- **THEN** `Foo.md` is the direct parent link (standard MD link)

#### Scenario: Inline TOC is not injected

- **WHEN** a class page has children (properties/methods)
- **THEN** no `<!-- toc:start -->` / `<!-- toc:end -->` block is written to the class page
- **THEN** the class page body retains the child links that were present in the original HTML
