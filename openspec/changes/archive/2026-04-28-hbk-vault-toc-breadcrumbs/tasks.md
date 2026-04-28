## 1. Подготовка модулей

- [x] 1.1 В `tools/hbk-to-md/convert.py` создать раздел «Pipeline post-processing» с двумя функциями-точками входа: `build_toc(out_dir, archive_index)` и `inject_breadcrumbs(out_dir, archive_index, tree)`
- [x] 1.2 Добавить словарь `SEGMENT_TITLES` (`methods` → "Методы", `properties` → "Свойства", `events` → "События", `ctors` → "Конструкторы", `objects` → "Объекты", `tables` → "Таблицы", `lang` → "Встроенный язык 1С", `Global context` → "Глобальный контекст")
- [x] 1.3 Добавить константы: `BREADCRUMB_SEPARATOR = " › "`, `ALPHA_GROUP_THRESHOLD = 50`, `INDEX_PREFIX = "_index"`, `BREADCRUMB_MARKER = "**↑** [Главная]"`

## 2. Построение дерева иерархии

- [x] 2.1 Реализовать `@dataclass TreeNode` с полями: `prefix: str` (source_path без расширения), `segment: str` (последний сегмент), `title: str`, `content_filename: Optional[str]` (имя content `.md`, если есть), `children: dict[str, TreeNode]`, `page_count: int` (рекурсивный счётчик leaf-страниц)
- [x] 2.2 Реализовать `build_hierarchy(archive_index: dict[str, str], pages_meta: dict[str, dict]) -> TreeNode`:
      - root = пустой TreeNode
      - для каждой записи `archive_index`: разбить путь на сегменты, спускаться по tree, создавать missing TreeNode'ы
      - на leaf-узле проставить `content_filename` и `title` (из frontmatter `title_ru`)
- [x] 2.3 Реализовать `propagate_titles(node: TreeNode)` — для internal node без content проставить title из `SEGMENT_TITLES.get(segment, segment)`; если есть парная content-страница — взять оттуда `title_ru`
- [x] 2.4 Реализовать `compute_page_counts(node: TreeNode) -> int` — рекурсивный подсчёт leaf-страниц для каждого узла (для отображения counts в `_index`)

## 3. Генерация `_index*.md`

- [x] 3.1 Реализовать `index_filename_for(prefix: str) -> str` — `prefix` ('objects/Global context/methods') → `_index__objects__Global_context__methods.md` (тот же алгоритм, что `archive_path_to_filename`, но с префиксом `_index__`)
- [x] 3.2 Реализовать `parent_index_for(prefix: str) -> Optional[str]` — путь до ближайшего вышестоящего `_index` (от родителя вверх до root); root → `_index.md`
- [x] 3.3 Реализовать `render_index(node: TreeNode, parent_index: Optional[str]) -> str`:
      - frontmatter (`type: index`, `source_prefix`, `parent_index`)
      - H1 = node.title
      - cross-link на content-страницу, если `node.content_filename` not None
      - секция `## Подразделы (N)` — children, у которых есть свои children; sort по title
      - секция `## Страницы (N)` — leaf-children; sort по title
      - алфавитная группировка (H3 по первой букве `title.casefold()`) если N > `ALPHA_GROUP_THRESHOLD`
      - в конце — breadcrumb (см. секцию 4)
- [x] 3.4 Реализовать `render_root_index(tree: TreeNode, hbk_version: str, total_pages: int) -> str`:
      - frontmatter (`type: index-root`, `hbk_version`, `total_pages`)
      - H1 «Vault: 1С:Предприятие <version> — справка»
      - статистика: общая + по hbk_source
      - секция `## Разделы` — top-level children с counts
      - breadcrumb-блока НЕТ
- [x] 3.5 Реализовать `write_all_indexes(tree: TreeNode, out_dir: Path) -> int` — обход дерева, для каждого internal node — `write_md(out_dir, index_filename_for(prefix), '', render_index(...))`; вернуть количество созданных файлов

## 4. Breadcrumb-генератор

- [x] 4.1 Реализовать `walk_parents(prefix: str) -> list[str]` — пути от корня до родителя текущего префикса (исключая сам префикс): `'objects/Global context/methods/catalog1566/CanReadXML1628'` → `['objects', 'objects/Global context', 'objects/Global context/methods', 'objects/Global context/methods/catalog1566']`
- [x] 4.2 Реализовать `resolve_breadcrumb_target(prefix: str, archive_index, index_filenames: set) -> Optional[tuple[str, str]]`:
      - lookup content `.md` в `archive_index` по `prefix.lower() + '.html'` и `prefix.lower()` — если найдено, вернуть (filename, title)
      - иначе lookup `_index__<prefix>.md` в `index_filenames` — если найдено, вернуть (filename, resolved_title)
      - иначе `None` (skip)
- [x] 4.3 Реализовать `render_breadcrumb(prefix: str, archive_index, index_filenames, tree) -> str`:
      - всегда начать с `**↑** [Главная](_index.md)`
      - для каждого parent prefix — добавить ` › ` + резолвленный линк (skip если None)
      - вернуть полную строку (одна строка)
- [x] 4.4 Реализовать `inject_breadcrumb_into_content(filepath: Path, breadcrumb: str) -> bool`:
      - читать файл; найти конец frontmatter (вторая `---` строка)
      - вставить `breadcrumb + '\n\n'` сразу после frontmatter, перед content
      - перезаписать файл; вернуть True если добавили (False если страница без frontmatter — пропустить)
- [x] 4.5 Реализовать `inject_all_breadcrumbs(tree: TreeNode, out_dir: Path, archive_index, index_filenames) -> int` — обход всех content-страниц, вставка breadcrumb; вернуть количество обработанных

## 5. Интеграция в pipeline

- [x] 5.1 В `main()` после `_convert_archive` (для shcntx и shlang) вызвать:
      ```python
      tree = build_hierarchy(archive_index, ...)
      propagate_titles(tree)
      compute_page_counts(tree)
      stats.index_files_generated = write_all_indexes(tree, out_dir)
      stats.index_files_generated += 1  # root _index.md
      write_root_index(tree, out_dir, hbk_version, stats.converted)
      stats.breadcrumbs_added = inject_all_breadcrumbs(tree, out_dir, archive_index, index_filenames)
      ```
- [x] 5.2 Добавить поля `index_files_generated: int = 0` и `breadcrumbs_added: int = 0` в `@dataclass Stats`; обновить `as_dict()`
- [x] 5.3 Обновить лог-строку в `main()` по завершении: добавить `index_files=N breadcrumbs=N`

## 6. Тесты

- [x] 6.1 Создать `tools/hbk-to-md/tests/test_toc.py`:
      - `test_build_hierarchy_simple` — 3 страницы, проверить дерево
      - `test_propagate_titles_known_segment` — `methods` → "Методы"
      - `test_propagate_titles_from_content_page` — title_ru из парной content-страницы
      - `test_index_filename_for` — `'objects/Global context/methods'` → `'_index__objects__Global_context__methods.md'`
      - `test_render_index_subsections_only` — рендер с секцией Подразделы
      - `test_render_index_pages_only` — рендер с секцией Страницы
      - `test_render_index_alpha_grouping` — N > 50 → группировка по буквам
      - `test_root_index_no_breadcrumb` — корневой `_index.md` без breadcrumb
      - `test_compute_page_counts` — рекурсивный подсчёт
- [x] 6.2 Создать `tools/hbk-to-md/tests/test_breadcrumbs.py`:
      - `test_walk_parents_deep` — 5-уровневая страница → 4 prefix'а
      - `test_resolve_target_content_priority` — content-страница приоритетнее `_index`
      - `test_resolve_target_index_fallback` — нет content → `_index`
      - `test_resolve_target_skip` — нет ни того ни другого → None
      - `test_render_breadcrumb_format` — полный breadcrumb с разделителем ` › `
      - `test_render_breadcrumb_root_only` — top-level страница (2 сегмента)
      - `test_inject_breadcrumb_after_frontmatter` — корректная вставка после `---`
      - `test_inject_breadcrumb_no_frontmatter` — страница без frontmatter не модифицируется
- [x] 6.3 `python -m pytest tools/hbk-to-md/tests/` — все тесты проходят (зелёные)

## 7. Проверка на реальных данных

- [x] 7.1 Запустить `python tools/hbk-to-md/convert.py --hbk ".../shcntx_ru.hbk" --lang-hbk ".../shlang_ru.hbk" --out _forResearch/hbk-vault --clean`
- [x] 7.2 Проверить `_meta.json`: `index_files_generated > 500`, `breadcrumbs_added == 25542`, `failed == 0`
- [x] 7.3 Открыть `_forResearch/hbk-vault/_index.md` — статистика и ссылки на 3 топ-секции
- [x] 7.4 Открыть `_forResearch/hbk-vault/_index__objects__Global_context__methods.md` — алфавитная группировка ~1500 методов
- [x] 7.5 Открыть `_forResearch/hbk-vault/objects__Global_context__methods__catalog1566__CanReadXML1628.md` — breadcrumb наверху корректный, кликается до `_index.md`, последний сегмент = «Группа методов» (родитель), не CanReadXML
- [x] 7.6 Проверить страницу с парной content+_index: `objects__catalog1649.md` (content) и `_index__objects__catalog1649.md` (index) — оба существуют, _index ссылается на content
- [x] 7.7 Проверить `_forResearch/hbk-vault/lang__def_String.md` — breadcrumb для shlang работает, ведёт через `[Главная]` › `[Встроенный язык 1С]` (через `_index__lang.md`)
- [x] 7.8 Открыть vault в Obsidian: `_index.md` отображается, навигация по линкам работает, breadcrumb наверху страниц кликабелен *(требует ручной проверки пользователя)*

## 8. Документация

- [x] 8.1 Дополнить `tools/hbk-to-md/README.md`: новый раздел «Навигация» с описанием `_index*.md` (структура, формат) и breadcrumb-блока (где, как читать)
- [x] 8.2 Добавить в README пример того, как скрыть `_index*.md` в Obsidian через `.obsidianignore` (опционально, для тех кто хочет видеть только content)
- [x] 8.3 Обновить запись в [AGENTS.md](AGENTS.md) — упомянуть, что vault имеет `_index.md` как точку входа

## 9. Token-optimized revision

- [x] 9.1 Изменить генерацию TOC: если у узла есть `content_filename`, НЕ создавать отдельный `_index__<prefix>.md`
- [x] 9.2 Реализовать встраивание блока `## Оглавление` в content-страницу раздела (после основного содержания)
- [x] 9.3 Обновить breadcrumbs для режима без frontmatter: вставка перед первым H1
- [x] 9.4 Удалять из output ссылки/блоки `Методическая информация` (включая `1centerprise.com/devlinks`)
- [x] 9.5 Убрать запись полей frontmatter (`title_ru`, `title_en`, `source_path`, `hbk_source`, `hbk_version`, `availability`) из итоговых content-файлов
- [x] 9.6 Добавить/обновить тесты на отсутствие `_index` при наличии content-страницы
- [x] 9.7 Добавить/обновить тесты на inline-оглавление в content-страницах
- [x] 9.8 Добавить/обновить тесты на удаление `Методическая информация`
- [x] 9.9 Добавить/обновить тесты на формат без frontmatter
- [x] 9.10 Перегенерировать `_forResearch/hbk-vault` и проверить: меньше `_index`-файлов, нет `Методическая информация`, нет frontmatter-полей
