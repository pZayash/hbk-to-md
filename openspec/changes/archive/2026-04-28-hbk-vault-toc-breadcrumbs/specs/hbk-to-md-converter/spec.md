## ADDED Requirements

### Requirement: Корневой `_index.md` как точка входа в vault

Конвертер SHALL генерировать в корне `--out` файл `_index.md` — точку входа в vault. Файл SHALL содержать YAML-frontmatter с `type: index-root`, заголовок с версией платформы 1С, статистику по количеству страниц и список ссылок на `_index__<top>.md` каждой top-секции (`objects`, `lang`, `tables` — те, для которых есть страницы).

#### Scenario: Базовая генерация `_index.md`

- **WHEN** конвертация завершена и в vault есть страницы из `shcntx_ru.hbk` (24 500) и `shlang_ru.hbk` (1 042)
- **THEN** в `--out/_index.md` создан файл с frontmatter `type: index-root`, `hbk_version: "8.3.27.1786"`, `total_pages: 25542`
- **THEN** в теле файла H1 содержит «1С:Предприятие <version> — справка»
- **THEN** в теле есть строка статистики «Всего страниц: **25 542**»
- **THEN** в теле есть секция «## Разделы» с пунктами-ссылками на `_index__objects.md`, `_index__lang.md`, `_index__tables.md`

#### Scenario: Топ-секция без страниц не добавляется

- **WHEN** в vault'е нет страниц для `tables/`
- **THEN** в `_index.md` нет ссылки на `_index__tables.md`

### Requirement: `_index__<prefix>.md` для каждого внутреннего узла иерархии

Конвертер SHALL генерировать файл `_index__<prefix>.md` для каждого префикса (внутреннего узла иерархии), у которого есть хотя бы один child. Префикс — `source_path` без расширения, с заменой `/` и пробелов на `__`/`_` соответственно (тот же алгоритм, что для content-страниц). Leaf-страницы (без children) SHALL NOT получать `_index`.

#### Scenario: Генерация `_index` для папки без своей content-страницы

- **WHEN** в vault есть страницы `objects/Global context/methods/catalog1566/CanReadXML1628.html` и др. (всего 12 файлов под `objects/Global context/methods/`)
- **THEN** в `--out/_index__objects__Global_context__methods.md` создан файл-индекс
- **THEN** в frontmatter `type: index`, `source_prefix: "objects/Global context/methods"`, `parent_index: "_index__objects__Global_context.md"` (или путь до ближайшего вышестоящего `_index`)

#### Scenario: Генерация `_index` для папки с парной content-страницей

- **WHEN** в vault есть `objects/Global context.html` (content-страница `objects__Global_context.md`) И есть дочерние страницы под `objects/Global context/`
- **THEN** генерируется `_index__objects__Global_context.md` параллельно с существующей `objects__Global_context.md`
- **THEN** content-страница `objects__Global_context.md` НЕ модифицируется (только добавляется breadcrumb наверху, см. отдельное требование)
- **THEN** в `_index__objects__Global_context.md` есть строка-ссылка на content-страницу: `[Содержание страницы раздела →](objects__Global_context.md)`

#### Scenario: Leaf-страница не получает `_index`

- **WHEN** страница `objects/Global context/methods/catalog1566/CanReadXML1628.html` не имеет вложенных страниц
- **THEN** файл `_index__objects__Global_context__methods__catalog1566__CanReadXML1628.md` НЕ создаётся

### Requirement: Содержимое `_index` — листинг direct children

Каждый `_index__<prefix>.md` SHALL содержать YAML-frontmatter (`type: index`, `source_prefix`, `parent_index`), заголовок H1 с title, опциональную ссылку на парную content-страницу (если есть) и листинг direct children. Children делятся на две группы:

1. **Подразделы** — direct-children, у которых сами есть дети (sub-sections); каждый — линк на свой `_index__<child>.md` с counts
2. **Страницы** — leaf-children; каждый — линк на content-страницу с `title_ru (title_en)` (если есть `title_en`)

В `_index` сначала идёт секция `## Подразделы (N)`, потом `## Страницы (N)`. Если одна из групп пуста — её секция отсутствует. Сортировка внутри секции — по `title_ru` (case-insensitive).

#### Scenario: Листинг подразделов и страниц

- **WHEN** под префиксом `objects/Global context` есть 3 sub-папки (`events`, `methods`, `properties`) и 0 leaf-страниц
- **THEN** в `_index__objects__Global_context.md` есть секция `## Подразделы (3)` со ссылками на `_index__objects__Global_context__events.md`, `_index__objects__Global_context__methods.md`, `_index__objects__Global_context__properties.md`
- **THEN** ссылки сопровождаются counts: например, `[Методы (1547 страниц)](_index__objects__Global_context__methods.md)`
- **THEN** секции `## Страницы` нет (leaf-children отсутствуют)

#### Scenario: Только leaf-страницы

- **WHEN** под префиксом `objects/Global context/methods/catalog1566` есть 4 метода и 0 sub-папок
- **THEN** в `_index__...__catalog1566.md` есть секция `## Страницы (4)` со ссылками на 4 метода
- **THEN** секции `## Подразделы` нет

### Requirement: Алфавитная группировка при N > 50

Если в секции `## Страницы` (или `## Подразделы`) больше 50 элементов, элементы SHALL группироваться по первой букве `title_ru` (case-insensitive). Каждая группа — подзаголовок H3 с буквой, под ним — список элементов.

#### Scenario: Группировка большого списка методов

- **WHEN** в `_index__objects__Global_context__methods.md` 1547 страниц
- **THEN** под `## Страницы (1547)` идут подзаголовки `### А`, `### Б`, ..., `### Я`, `### A`, ... `### Z`
- **THEN** под каждым H3 — список страниц на эту букву

#### Scenario: Малый список без группировки

- **WHEN** в `_index__...__catalog1566.md` 4 страницы (≤50)
- **THEN** под `## Страницы (4)` идёт плоский список без подзаголовков H3

### Requirement: Resolved title для `_index` без парной content-страницы

Для префиксов без парной content-страницы (`methods/`, `properties/`, `events/`, `objects/`, `tables/`, `lang/`, etc.) title SHALL быть взят из словаря известных segment'ов (`methods` → "Методы", `properties` → "Свойства", `events` → "События", `ctors` → "Конструкторы", `objects` → "Объекты", `tables` → "Таблицы", `lang` → "Встроенный язык 1С", `Global context` → "Глобальный контекст"). Для неизвестных segment'ов title = сам segment.

#### Scenario: Известный segment

- **WHEN** генерируется `_index__objects__Global_context__methods.md`
- **THEN** H1 файла = `# Методы`

#### Scenario: Неизвестный segment без парной страницы

- **WHEN** генерируется `_index__objects__SomeUnknownFolder.md` и `objects__SomeUnknownFolder.md` НЕ существует
- **THEN** H1 файла = `# SomeUnknownFolder`

#### Scenario: Парная content-страница есть

- **WHEN** генерируется `_index__objects__catalog1649.md` и `objects__catalog1649.md` содержит `title_ru: "Интерфейс"`
- **THEN** H1 файла = `# Интерфейс`

### Requirement: Breadcrumb-блок наверху content-страницы

После основной конвертации каждая content-страница (`objects__*.md`, `lang__*.md`, `tables__*.md`) SHALL получить блок-breadcrumb наверху — строго после frontmatter (`---\n...\n---`), перед H1, отделённый пустой строкой. Формат: `**↑** [Главная](_index.md) › <segment1> › <segment2> › ...`. Разделитель — ` › ` (U+203A).

Walk родителей по `source_path`: для каждого префикса (от корня до родителя текущей страницы) SHALL резолвиться таргет:

1. Если есть content-страница для префикса (lookup в архивном индексе) → линк на неё с `title_ru` как text
2. Иначе если есть `_index__<prefix>.md` → линк на `_index` с resolved title (см. отдельное требование)
3. Иначе segment SHALL пропускаться (skip)

Корневой элемент `[Главная](_index.md)` всегда присутствует. Текущая страница (последний segment) НЕ включается в breadcrumb (она видна как H1 ниже).

#### Scenario: Breadcrumb для глубокой страницы со всеми резолвами

- **WHEN** конвертируется `objects/Global context/methods/catalog1566/CanReadXML1628.html`
- **WHEN** `objects/Global context.html` есть как content; `objects/Global context/methods/` нет content, но есть `_index__objects__Global_context__methods.md`; `objects/Global context/methods/catalog1566.html` есть как content; `objects/` не имеет content, но имеет `_index__objects.md`
- **THEN** в начале `objects__Global_context__methods__catalog1566__CanReadXML1628.md` (после frontmatter, перед H1) есть строка: `**↑** [Главная](_index.md) › [Объекты](_index__objects.md) › [Глобальный контекст](objects__Global_context.md) › [Методы](_index__objects__Global_context__methods.md) › [Группа методов](objects__Global_context__methods__catalog1566.md)`
- **THEN** между breadcrumb и H1 — одна пустая строка

#### Scenario: Skip сегмента без content и без `_index`

- **WHEN** для префикса `objects/SomeOrphan/` нет ни content `.md` ни `_index__objects__SomeOrphan.md`
- **THEN** этот сегмент пропускается в breadcrumb (skip), остальные сегменты сохраняются

#### Scenario: Текущая страница не входит в breadcrumb

- **WHEN** конвертируется страница `objects__catalog1649__catalog1890__ClientApplicationForm.md`
- **THEN** последний элемент breadcrumb — НЕ ClientApplicationForm, а его родитель «Форма клиентского приложения»

#### Scenario: Top-level страница (2 сегмента)

- **WHEN** конвертируется `objects/Global context.html` (страница уровня 2: `objects__Global_context.md`)
- **THEN** breadcrumb = `**↑** [Главная](_index.md) › [Объекты](_index__objects.md)`

### Requirement: Breadcrumb-блок наверху `_index` файлов

Каждый `_index__<prefix>.md` (кроме корневого `_index.md`) SHALL получить breadcrumb-блок в конце файла (после листинга children) с тем же форматом и тем же resolved walk, что и для content-страниц. Корневой `_index.md` breadcrumb НЕ имеет.

#### Scenario: Breadcrumb на _index файле

- **WHEN** генерируется `_index__objects__Global_context__methods.md`
- **THEN** в конце файла блок: `**↑** [Главная](_index.md) › [Объекты](_index__objects.md) › [Глобальный контекст](objects__Global_context.md)`

#### Scenario: Breadcrumb на корневом _index отсутствует

- **WHEN** генерируется `_index.md`
- **THEN** breadcrumb-блока в файле нет (корень — некуда подниматься)

### Requirement: Статистика TOC и breadcrumbs в `_meta.json`

Файл `_meta.json` SHALL содержать дополнительные поля статистики:

- `index_files_generated` — количество созданных `_index*.md` файлов (включая корневой)
- `breadcrumbs_added` — количество content-страниц, получивших breadcrumb-блок

#### Scenario: Поля статистики записаны

- **WHEN** конвертация завершена и сгенерировано 712 `_index*.md` файлов; 25 542 content-страницы получили breadcrumb
- **THEN** в `_meta.json.stats` есть `"index_files_generated": 712, "breadcrumbs_added": 25542`

### Requirement: Не создавать `_index` для узлов с парной content-страницей

Конвертер SHALL НЕ создавать `_index__<prefix>.md`, если для этого `prefix` существует content-страница (`objects__...`, `tables__...`, `lang__...`).  
Для таких узлов оглавление SHALL рендериться прямо в content-странице.

#### Scenario: `objects/catalog2` без отдельного `_index`

- **WHEN** существует content `objects__catalog2.md` и у префикса `objects/catalog2` есть children
- **THEN** файл `_index__objects__catalog2.md` НЕ создаётся
- **THEN** в `objects__catalog2.md` после основного текста добавлен блок `## Оглавление` с подразделами/страницами

### Requirement: Удаление ссылок «Методическая информация»

Конвертер SHALL удалять из итогового markdown блоки и ссылки «Методическая информация», ведущие на `1centerprise.com/devlinks`.

#### Scenario: Ссылка внизу страницы удалена

- **WHEN** исходная HTML-страница содержит внизу ссылку «Методическая информация»
- **THEN** в итоговом `.md` отсутствует текст `Методическая информация`
- **THEN** отсутствует ссылка на `http://www.1centerprise.com/devlinks?...`

### Requirement: Минимизация frontmatter для token-optimized выгрузки

Итоговые content-файлы SHALL не содержать YAML-frontmatter с полями `title_ru`, `title_en`, `source_path`, `hbk_source`, `hbk_version`, `availability`.

#### Scenario: Content без мета-полей

- **WHEN** конвертирована страница `objects/...`
- **THEN** в начале файла нет блока `--- ... ---` с перечисленными полями
- **THEN** файл начинается с breadcrumb (если включён) и/или `# <заголовок>`
