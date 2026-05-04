## Context

`build_archive_index` does a single pass over all HTML files: for each file it computes a title-based filename and stores `rel_path.lower() → filename` in the index. When two files share the same H1 title (e.g. "Ссылка (Ref)"), both entries map to the same filename string. This index is then used by `rewrite_links` to resolve targets — so every link pointing to *any* of the colliding files resolves to the same (wrong) file. Disambiguation (`-2`, `-3`) happens in `convert_one` at write time, after link rewriting is already done, producing orphan files with no inbound links.

Current stats on `shcntx_ru.hbk` 8.3.27.1786: **638 collisions**. Top sources: `<Имя общего реквизита>` (46×), `Регистратор` (28×), `Ссылка (Ref)` (22×), `НомерСтроки` (21×), `Период` (20×).

Archive path structure for colliding pages:
```
tables/
  table6.html       ← "Каталог.<Имя справочника> (Catalog.<Имя справочника>)"
  table6/fields/Ref38.html          ← "Ссылка (Ref)"   [COLLISION]
  table81.html      ← "ВнешнийИсточникДанных...ТаблицаИзмерения..."
  table81/fields/Ref645.html        ← "Ссылка (Ref)"   [COLLISION]
  catalog63/
    table66.html    ← "Документ.<Имя>.Изменения (Document.<Имя>.Changes)"
    table66/fields/Ref546.html      ← "Ссылка (Ref)"   [COLLISION]
    table67.html    ← "ПланВидовХарактеристик.<Имя>.Изменения (...)"
    table67/fields/Ref549.html      ← "Ссылка (Ref)"   [COLLISION]
```

For every colliding file there exists a sibling `.html` at the parent directory level with a unique, semantically meaningful title.

## Goals / Non-Goals

**Goals:**
- Each `rel_path` in `archive_index` maps to a **unique** filename before `rewrite_links` runs
- Colliding pages get semantic parent-enriched names consistent with existing naming convention (`Parent.Child_(En.En).md`)
- All inbound links in the vault point to the correct file
- No change to non-colliding pages

**Non-Goals:**
- Renaming files that currently have unique title-based names
- Handling collisions in index pages (those go through a separate `compute_index_name_map` path)
- Full elimination of `disambiguate` — it stays as a safety net

## Decisions

### Decision 1: Two-pass `build_archive_index`

**Chosen:** Pass 1 collects `(rel_path, title)` pairs and counts title occurrences. Pass 2 assigns filenames — unique titles use `title_to_filename`, colliding titles use parent enrichment.

**Alternative considered:** Single-pass with a `seen` set and immediate rename on collision. Rejected because we need to know *all* occurrences upfront to treat the *first* occurrence of a colliding title correctly (it should also get the enriched name, not the plain one).

### Decision 2: Parent resolution via sibling-HTML walk

**Chosen:** For a colliding file at `a/b/c/file.html`, walk up: try `a/b/c.html`, then `a/b.html`, then `a.html`. Use the first match found in `title_map`. Combine as `parent_title + "." + child_title`, then call `title_to_filename`.

```python
def resolve_parent_title(rel_path: str, title_map: dict[str, str]) -> str:
    parts = rel_path.split("/")
    for i in range(len(parts) - 2, 0, -1):
        candidate = "/".join(parts[:i]) + ".html"
        title = title_map.get(candidate.lower(), "")
        if title:
            return title
    return ""
```

**Alternative considered:** Using archive path segments directly (e.g., `table6__Ref38.md`). Rejected — numeric IDs (`table6`, `Ref38`) are not human-readable.

**Alternative considered:** Building the tree first, then back-filling filenames. Rejected — tree is built *after* `archive_index`, restructuring the pipeline is a larger change.

### Decision 3: Combine as `parent_title + "." + child_title`

**Chosen:** String concatenation with `.` separator before calling `title_to_filename`. This naturally produces the `Родитель.Имя_(Parent.Name).md` pattern already used by pages where the H1 already contains the full path.

**Result examples:**
- `tables/table6/fields/Ref38.html` → `Каталог.Имя_справочника_(Catalog.Имя_справочника).Ссылка_(Ref).md`
- `tables/table81/fields/Ref645.html` → `ВнешнийИсточникДанных...ТаблицаИзмерения...Ссылка_(Ref).md` (truncated by existing `truncate_filename`)

### Decision 4: `title_map` required for collision path

`build_archive_index` already accepts `title_map: dict[str, str] | None`. The parent-resolution walk uses this same map. No new pre-scan pass needed — the caller already runs `quick_scan_titles` for `shcntx`.

**Edge case:** If `title_map is None` (shlang archive), skip enrichment and fall back to `archive_path_to_filename`. Shlang collision rate is much lower (language reference pages tend to have unique names like `lang__def_String`).

## Risks / Trade-offs

**Enriched names are longer** → existing `truncate_filename` (MAX_FILENAME chars, SHA1 suffix) handles this. No change needed.

**Second-level collision** (two colliding files share the same parent title) → `disambiguate` adds `-2` suffix as before. Expected to be rare or zero in practice — confirmed by exploring `catalog63/table66` vs `catalog63/table67` which have distinct parent titles.

**Order-sensitivity eliminated** → previously the first file processed "won" the clean name; now all colliding files get enriched names regardless of processing order. This is an improvement.

**Vault churn** → existing `Ссылка_(Ref)-2.md` … `-22.md` files are replaced with semantic names. All inbound links are regenerated correctly on next conversion run. No incremental migration needed — conversion is always a full rebuild (`--clean`).

## Migration Plan

1. Implement two-pass `build_archive_index` in `convert.py`
2. Update `test_filename.py` collision scenarios
3. Re-run full conversion; verify `_collisions.log` count drops significantly (residual entries = true second-level collisions only)
4. Replace vault output

No rollback needed — vault is regenerated from source HBK on every run.

## Open Questions

_(none)_
