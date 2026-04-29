## MODIFIED Requirements

### Requirement: YAML-frontmatter в каждом `.md`

Итоговые Markdown-файлы SHALL НЕ содержать YAML-frontmatter. Ни content-файлы, ни `_index.md`, ни `_index__*.md` НЕ MUST начинаться с блока `--- ... ---`.

#### Scenario: Content-файл без frontmatter
- **WHEN** конвертируется страница с заголовком `Глобальный контекст.ВозможностьЧтенияXML`
- **THEN** итоговый `.md` не содержит стартовый блок `--- ... ---`
- **THEN** файл начинается с `# Глобальный контекст.ВозможностьЧтенияXML` (или с тела, если H1 отсутствует)

#### Scenario: Index-файл без frontmatter
- **WHEN** генерируется `_index.md` и `_index__Объекты.md`
- **THEN** в начале файлов отсутствует YAML-блок `--- ... ---`
- **THEN** файлы содержат только markdown-контент и навигационные секции

### Requirement: Корневой `_index.md` как точка входа в vault

Конвертер SHALL генерировать в корне `--out` файл `_index.md` как human-readable точку входа в vault. Файл SHALL содержать H1 с версией платформы 1С, статистику по количеству страниц и список ссылок на top-секции (`objects`, `lang`, `tables`) — без YAML-frontmatter.

#### Scenario: Базовая генерация `_index.md`
- **WHEN** конвертация завершена и в vault есть страницы из `shcntx_ru.hbk` (24 500) и `shlang_ru.hbk` (1 042)
- **THEN** в `--out/_index.md` есть H1 с версией платформы
- **THEN** в теле есть строка статистики `Всего страниц: **25 542**`
- **THEN** в теле есть секция `## Разделы` со ссылками на top-level index-файлы
- **THEN** файл не содержит frontmatter-полей `type`, `hbk_version`, `total_pages`

### Requirement: Содержимое `_index` — листинг direct children

Каждый `_index__<prefix>.md` SHALL содержать заголовок H1 с title, опциональную ссылку на парную content-страницу (если есть) и листинг direct children в двух группах: подразделы и страницы. YAML-frontmatter (`type`, `source_prefix`, `parent_index`) SHALL NOT записываться в файл.

#### Scenario: Листинг подразделов и страниц
- **WHEN** под префиксом `objects/Global context` есть 3 sub-папки (`events`, `methods`, `properties`) и 0 leaf-страниц
- **THEN** в `_index__objects__Global_context.md` есть секция `## Подразделы (3)` со ссылками на соответствующие target-файлы
- **THEN** секции `## Страницы` нет
- **THEN** файл не содержит frontmatter `type: index`, `source_prefix`, `parent_index`

### Requirement: Breadcrumb-блок наверху content-страницы

После основной конвертации каждая content-страница (`objects__*.md`, `lang__*.md`, `tables__*.md`) SHALL получить breadcrumb-блок после H1, перед телом страницы, отделённый пустой строкой. Формат breadcrumb: `**↑** [Главная](_index.md) › <segment1> › <segment2> › ...`.

#### Scenario: Breadcrumb для глубокой страницы со всеми резолвами
- **WHEN** конвертируется `objects/Global context/methods/catalog1566/CanReadXML1628.html`
- **THEN** в `objects__...__CanReadXML1628.md` первая строка — H1 текущей страницы
- **THEN** breadcrumb расположен сразу после H1 и одной пустой строки
- **THEN** между breadcrumb и телом страницы одна пустая строка

### Requirement: Структура контента — H1 до breadcrumb

Каждый content-файл SHALL иметь следующий порядок:
1. `# {title}` (если заголовок распознан)
2. Пустая строка
3. Breadcrumb-строка (если генерируется)
4. Пустая строка
5. Тело страницы

Frontmatter-слой в структуру НЕ входит.

#### Scenario: Файл открывается на H1
- **WHEN** конвертируется страница с `title_ru = "Глобальный контекст.ВозможностьЧтенияXML"` и breadcrumb активирован
- **THEN** первая строка файла: `# Глобальный контекст.ВозможностьЧтенияXML`
- **THEN** следующая непустая строка после H1 — breadcrumb

#### Scenario: Страница без breadcrumb — H1 первая строка
- **WHEN** страница не имеет breadcrumb (нет `_index`-pass)
- **THEN** первая строка файла: `# {title_ru}`
- **THEN** файл не содержит frontmatter перед H1

### Requirement: Минимизация frontmatter для token-optimized выгрузки

Итоговые `.md`-файлы SHALL полностью исключать YAML-frontmatter для token-optimized выгрузки. Запрещены как “полные” поля (`title_ru`, `title_en`, `source_path`, `hbk_source`, `hbk_version`, `availability`), так и “минимальные” (`title`, `type`, `source_prefix`, `parent_index`, `total_pages`).

#### Scenario: Ни один `.md` не содержит YAML frontmatter
- **WHEN** конвертация завершена
- **THEN** любой output-файл с расширением `.md` не начинается с `---`
- **THEN** технические метаданные доступны через `_meta.json`, а не через frontmatter
