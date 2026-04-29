## 1. Primitive Type Suppression (convert.py + signatures.py)

- [x] 1.1 Add `PRIMITIVE_TYPE_STEMS: frozenset[str]` constant in `convert.py` with the full list of primitive-type page stems (case-insensitive)
- [x] 1.2 In `rewrite_links`, after resolving `target_filename`, check if its stem is in `PRIMITIVE_TYPE_STEMS`; if so, replace the `<a>` tag with its plain text content (no link emitted)
- [x] 1.3 In `signatures.py`, add a helper `is_primitive(link: str) -> bool` that checks the stem against `PRIMITIVE_TYPE_STEMS`
- [x] 1.4 In `render_type_tokens` (`signatures.py`), use `is_primitive` — emit `` `Name` `` without link when target is primitive
- [x] 1.5 Update `test_parse.py` / `test_signatures.py` to cover primitive suppression cases

## 2. Segment Index Suppression (convert.py)

- [x] 2.1 Add `SKIP_SEGMENT_INDEX: frozenset[str]` constant = `{"properties", "methods", "events", "ctors", "fields", "params", "formparams"}`
- [x] 2.2 In `build_index_name_map`, skip nodes where `node.segment in SKIP_SEGMENT_INDEX` (no entry added to `index_name_map`)
- [x] 2.3 In `write_all_indexes`, skip nodes where `node.segment in SKIP_SEGMENT_INDEX` (no `.md` file written)
- [x] 2.4 Verify that `render_breadcrumb` naturally skips segment nodes (they have no entry in `index_name_map`, so `resolve_breadcrumb_target` returns `None`)
- [x] 2.5 Update `test_toc.py` — assertions about `__Свойства.md` / `__Методы.md` file generation must be removed or inverted

## 3. Inline TOC — только для сегментных страниц (convert.py)

<!-- ПЕРЕСМОТРЕНО: страницы без прямых ссылок на детей (Общие_объекты и т.п.) нуждаются в TOC;
     TOC убирается только там где сегментный узел (__Свойства/__Методы) — такие страницы теперь не генерируются вовсе (задача 2).
     Функции render_inline_toc / inject_inline_toc_into_content остаются. -->
- [x] 3.1 В `inject_all_breadcrumbs` вызов `inject_inline_toc_into_content` оставить, но только для узлов где `node.segment NOT IN SKIP_SEGMENT_INDEX` — сегментные узлы уже не генерируют страницы (задача 2), поэтому их TOC сам по себе исчезает
- [x] 3.2 Убедиться что `render_inline_toc` и `inject_inline_toc_into_content` не удалены — они нужны для страниц-разделов без прямых ссылок (Общие_объекты и т.п.)
- [x] 3.3 Обновить `test_toc.py` — проверить что TOC генерируется для раздела без прямых ссылок и НЕ генерируется для страниц сегментного уровня (которых теперь нет)

## 4. Breadcrumb HTML Anchor Format (convert.py)

<!-- ПЕРЕСМОТРЕНО 4.1/4.2/4.7: хлебные крошки включены по умолчанию — найден хороший способ отображения через HTML-анкоры;
     флаг переименован в --no-breadcrumbs для отключения. -->
- [x] 4.1 Добавить флаг `--no-breadcrumbs` (store_true) в `argparse`; по умолчанию хлебные крошки ВКЛЮЧЕНЫ
- [x] 4.2 В `main()` оборачивать `run_stage(STAGE_INJECT_BREADCRUMBS, ...)` условием `if not args.no_breadcrumbs:`
- [x] 4.3 В `render_breadcrumb` разделить предков на "все кроме последнего" (HTML-анкоры) и "последний" (MD-ссылка)
- [x] 4.4 Домашняя ссылка (`_index.md`) → `**↑** <a href="obsidian://open?file=_index.md">Главная</a>`
- [x] 4.5 Промежуточные предки → `<a href="obsidian://open?file=FILENAME">title</a>`
- [x] 4.6 Прямой родитель (последний) → `[title](filename)` стандартная MD-ссылка
- [x] 4.7 Обновить `test_breadcrumbs.py` — проверить HTML-анкоры для предков, MD-ссылку для родителя; проверить что хлебные крошки есть без флагов и отсутствуют при `--no-breadcrumbs`

## 5. Integration Verification

- [x] 5.1 Run full conversion on a real `.hbk` sample with `--breadcrumbs` and verify: no `*__Свойства.md` files, no inline TOC blocks, breadcrumb has 1 MD link per page
- [x] 5.2 Run `python count_links.py vault` and confirm top hubs (`_index.md`, primitive types) have dramatically fewer incoming links
- [x] 5.3 Run full test suite (`pytest`) — all tests pass
