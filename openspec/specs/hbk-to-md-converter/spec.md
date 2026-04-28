## Purpose

Define behavior of the HBK to Markdown conversion pipeline and vault output format.

## Requirements


### Requirement: CLI-конвертер `.hbk` → плоский каталог `.md`

Система SHALL предоставлять Python-скрипт `tools/hbk-to-md/convert.py`, который принимает путь к `shcntx_ru.hbk` и (опционально) `shlang_ru.hbk` и записывает в указанный выходной каталог набор Markdown-файлов — по одному на каждую HTML-страницу справки.

#### Scenario: Базовый запуск с одним архивом

- **WHEN** вызван `python convert.py --hbk PATH/shcntx_ru.hbk --out PATH/vault --clean`
- **THEN** в `PATH/vault/` создан набор `.md`-файлов — по одному на каждую HTML-страницу из `shcntx_ru.hbk`
- **THEN** в `PATH/vault/_meta.json` записаны параметры запуска и статистика конвертации

#### Scenario: Запуск с обоими архивами

- **WHEN** вызван `python convert.py --hbk shcntx_ru.hbk --lang-hbk shlang_ru.hbk --out vault --clean`
- **THEN** в `vault/` присутствуют файлы из обоих архивов; страницы из `shlang_ru.hbk` имеют префикс `lang__`

#### Scenario: Отказ при непустом выходном каталоге без --clean

- **WHEN** `--out` указывает на непустой каталог и `--clean` не передан
- **THEN** скрипт завершается с ненулевым кодом и сообщением об ошибке
- **THEN** файлы в `--out` не модифицируются

### Requirement: Распаковка через pip-зависимости без внешних бинарей

Конвертер SHALL извлекать содержимое `.hbk` через pip-пакеты (без вызова внешних утилит `7z`, `unzip`, `V8unpack`). `.hbk` — V8 storage container, разворачивается двухступенчато: сначала `onec_dtools.ContainerReader` извлекает внутренние файлы V8 (включая `FileStorage`), затем `zipfile` стандартной библиотеки распаковывает `FileStorage` (обычный ZIP с HTML).

#### Scenario: V8 storage контейнер распакован

- **WHEN** на вход подан `shcntx_ru.hbk` (V8 storage с заголовком `FF FF FF 7F 00 02 00 00 ...`)
- **THEN** `onec_dtools.ContainerReader.extract(deflate=False, recursive=True)` создаёт во временной директории файлы `Book`, `FileStorage`, `IndexMainData`, `IndexPackBlock`, `MainData`, `PackBlock`, `PackLookup`
- **THEN** `FileStorage` начинается с PKZIP-сигнатуры `50 4B 03 04` и читается через `zipfile.ZipFile`
- **THEN** все HTML-страницы из `FileStorage` распакованы в выходной каталог распаковки

#### Scenario: Файлы внутри shlang без расширения распознаны как HTML

- **WHEN** в `shlang_ru.hbk/FileStorage` есть файлы `def_String`, `def_Number`, `def_Boolean` без расширения
- **THEN** конвертер определяет их как HTML по сигнатуре `<HTML` / `<!DOCTYPE` (с учётом UTF-8 BOM)
- **THEN** файлы попадают в `archive_index` и конвертируются в `lang__def_String.md` и т.п.

#### Scenario: Файлы `.st` (variant-syntax) пропускаются

- **WHEN** в `FileStorage` есть файлы с расширением `.st`
- **THEN** конвертер их игнорирует (V2-задача)

### Requirement: Плоская раскладка `.md` с кодированием иерархии в имени

Все `.md`-файлы SHALL находиться в корне выходного каталога. Иерархия исходных путей SHALL отражаться в именах файлов через разделитель `__` (двойное подчёркивание); пробелы внутри сегмента SHALL заменяться на `_`; расширение `.html` SHALL заменяться на `.md`.

#### Scenario: Преобразование вложенного пути

- **WHEN** в архиве файл `objects/Global context/methods/catalog1566/CanReadXML1628.html`
- **THEN** в `--out` создан файл `objects__Global_context__methods__catalog1566__CanReadXML1628.md`

#### Scenario: Преобразование пути без вложенности

- **WHEN** в архиве файл `objects/catalog56.html`
- **THEN** в `--out` создан файл `objects__catalog56.md`

#### Scenario: Префикс для второго архива

- **WHEN** конвертируется `shlang_ru.hbk` со страницей `def_String`
- **THEN** в `--out` создан файл `lang__def_String.md`

#### Scenario: Обрезка длинного имени

- **WHEN** результирующее имя файла превышает 200 символов
- **THEN** имя обрезается, в хвост добавляется `__TRUNC_<sha1[:8]>` исходного пути
- **THEN** соответствие исходного пути и итогового имени логируется в `_truncated.log`

#### Scenario: Коллизия имён после нормализации

- **WHEN** два разных исходных пути после нормализации дают одинаковое имя
- **THEN** ко второму и далее добавляется суффикс `-2`, `-3`, ...
- **THEN** коллизия логируется в `_collisions.log`

### Requirement: Переписывание внутренних ссылок в относительные `.md`

Все ссылки `v8help://...` внутри HTML-страниц SHALL быть переписаны в относительные Markdown-ссылки на соответствующие `.md`-файлы выходного каталога. Якоря `#section` после пути SHALL сохраняться. Внешние `http(s)://`-ссылки SHALL оставаться без изменений. Битые `<a href=http://...>` без кавычек на атрибуте SHALL быть удалены (тег заменён на текстовое содержимое).

#### Scenario: Ссылка SyntaxHelperContext с якорем

- **WHEN** в HTML встречается `<a href="v8help://SyntaxHelperContext/objects/X/Y.html#anchor">Title</a>`
- **THEN** в выходном MD ссылка имеет вид `[Title](objects__X__Y.md#anchor)`

#### Scenario: Ссылка SyntaxHelperLanguage

- **WHEN** в HTML встречается `<a href="v8help://SyntaxHelperLanguage/def_String">Строка</a>`
- **THEN** в выходном MD ссылка имеет вид `[Строка](lang__def_String.md)`

#### Scenario: Внешняя HTTP-ссылка

- **WHEN** в HTML встречается `<a href="https://example.com">Site</a>`
- **THEN** в выходном MD ссылка имеет вид `[Site](https://example.com)` — без изменений

#### Scenario: Битая ссылка «Методическая информация»

- **WHEN** в HTML встречается `<a href=http://www.1centerprise.com/devlinks?C="id=...";lan=ru" target="_blank">Методическая информация</a>`
- **THEN** тег `<a>` удалён; в выходном MD остаётся текст `Методическая информация` без ссылки

#### Scenario: Ссылка на отсутствующий целевой файл

- **WHEN** ссылка указывает на `v8help://...` с путём, которого нет в общем индексе
- **THEN** ссылка всё равно записывается в MD (в виде ожидаемого имени файла) — для возможного будущего пополнения vault'а
- **THEN** случай логируется в `_unresolved.log`

### Requirement: YAML-frontmatter в каждом `.md`

Каждый сгенерированный `.md`-файл SHALL начинаться с YAML-блока frontmatter, содержащего минимальный набор полей:

- `title_ru` — русское имя страницы из `<h1 class="V8SH_pagetitle">` (часть до круглых скобок)
- `title_en` — английское имя из тех же скобок (пустая строка, если не найдено)
- `source_path` — относительный путь файла внутри `.hbk`-архива
- `hbk_source` — `shcntx_ru` или `shlang_ru`
- `hbk_version` — версия платформы 1С (из `--version` или из имени каталога bin)
- `availability` — минимальная версия из `<p class="V8SH_versionInfo">`, если найдена; иначе поле отсутствует

#### Scenario: Полный frontmatter

- **WHEN** конвертируется страница `objects/Global context/methods/catalog1566/CanReadXML1628.html` с titles `Глобальный контекст.ВозможностьЧтенияXML (Global context.CanReadXML)` и version `8.0`
- **THEN** в начале выходного MD-файла блок:
  ```yaml
  ---
  title_ru: "Глобальный контекст.ВозможностьЧтенияXML"
  title_en: "Global context.CanReadXML"
  source_path: "objects/Global context/methods/catalog1566/CanReadXML1628.html"
  hbk_source: "shcntx_ru"
  hbk_version: "8.3.25.1445"
  availability: "8.0"
  ---
  ```

#### Scenario: Заголовок без английского варианта

- **WHEN** в `<h1 class="V8SH_pagetitle">` нет круглых скобок
- **THEN** `title_en` имеет значение пустой строки

#### Scenario: Версия не найдена

- **WHEN** в HTML нет `<p class="V8SH_versionInfo">` с шаблоном `8.X[.Y]`
- **THEN** поле `availability` отсутствует во frontmatter

### Requirement: Идемпотентность и логи запуска

Конвертер SHALL поддерживать повторный безопасный запуск через `--clean`. По завершении SHALL создавать в `--out` служебные файлы:

- `_meta.json` — параметры запуска, статистика (всего страниц, сконвертировано, ошибок, обрезанных имён, нерезолвленных ссылок), длительность
- `_truncated.log` — обрезанные имена (orig_path → final_name)
- `_collisions.log` — коллизии после нормализации
- `_unresolved.log` — ссылки на отсутствующие таргеты
- `_errors.log` — ошибки конвертации отдельных страниц (с путём и текстом исключения)

#### Scenario: Повторный запуск с --clean

- **WHEN** скрипт запущен с `--clean` на ранее использованный `--out`
- **THEN** содержимое `--out` полностью удалено
- **THEN** vault создан заново с нуля
- **THEN** сгенерирован новый `_meta.json`

#### Scenario: Ошибка одной страницы не прерывает остальные

- **WHEN** при конвертации одной из 25 000 страниц возникает исключение
- **THEN** ошибка записана в `_errors.log` (путь страницы + текст исключения)
- **THEN** остальные страницы конвертируются успешно
- **THEN** в `_meta.json.failed` отражено количество ошибок


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


### Requirement: Плоская раскладка `.md` с кодированием иерархии в имени

Все `.md`-файлы SHALL находиться в корне выходного каталога. Имена файлов SHALL быть производными от `title_ru` страницы (человекочитаемые), а не от пути в архиве. Пробелы SHALL заменяться на `_`; небезопасные символы (`/\:*?"<>|`) SHALL удаляться; расширение SHALL быть `.md`. Для страниц без заголовка допускается резервный (fallback) вариант — имя, производное от пути (через `archive_path_to_filename()`).

Страницы из `shlang_ru.hbk` SHALL сохранять префикс `lang__` перед title-derived частью имени.

#### Scenario: Метод получает имя по title_ru

- **WHEN** страница имеет `<h1 class="V8SH_pagetitle">Глобальный контекст.ВозможностьЧтенияXML (Global context.CanReadXML)</h1>`
- **THEN** в `--out` создан файл `Глобальный_контекст.ВозможностьЧтенияXML.md`

#### Scenario: Страница без заголовка — резервный вариант имени

- **WHEN** страница не имеет элемента `<h1 class="V8SH_pagetitle">`
- **THEN** имя файла производится из пути архива (поведение `archive_path_to_filename()`)

#### Scenario: Страница shlang получает title-имя с префиксом lang__

- **WHEN** конвертируется страница из `shlang_ru.hbk` с заголовком `"Строка"`
- **THEN** в `--out` создан файл `lang__Строка.md`

#### Scenario: Обрезка длинного имени

- **WHEN** результирующее имя файла превышает 200 символов
- **THEN** имя обрезается, в хвост добавляется `__TRUNC_<sha1[:8]>` исходного пути
- **THEN** соответствие исходного пути и итогового имени логируется в `_truncated.log`

#### Scenario: Коллизия имён после нормализации по title

- **WHEN** два разных исходных пути после title-нормализации дают одинаковое имя
- **THEN** ко второму и далее добавляется суффикс `-2`, `-3`, ...
- **THEN** коллизия логируется в `_collisions.log`

### Requirement: YAML-frontmatter в каждом `.md`

Каждый сгенерированный `.md`-файл SHALL начинаться с YAML-блока frontmatter, содержащего одно поле:

- `title` — полный русский заголовок страницы из `<h1 class="V8SH_pagetitle">` (полный текст до PAGETITLE_SPLIT_RE, т.е. `title_ru`; если пусто — `title_en`)

Остальные поля (`source_path`, `hbk_source`, `hbk_version`, `availability`) хранятся только в памяти и в `_meta.json`. Они НЕ SHALL записываться во frontmatter выходных `.md`.

#### Scenario: Frontmatter содержит только title

- **WHEN** конвертируется страница с `title_ru = "Глобальный контекст.ВозможностьЧтенияXML"`
- **THEN** в начале выходного MD-файла блок:
  ```yaml
  ---
  title: "Глобальный контекст.ВозможностьЧтенияXML"
  ---
  ```
- **THEN** поля `source_path`, `hbk_source`, `hbk_version` отсутствуют во frontmatter

#### Scenario: Заголовок без русского варианта

- **WHEN** `title_ru` пуст, но `title_en` не пуст
- **THEN** frontmatter содержит `title: "<title_en value>"`

#### Scenario: Страница без заголовка — frontmatter отсутствует

- **WHEN** страница не имеет распознанного заголовка (`title_ru` и `title_en` оба пусты)
- **THEN** frontmatter блок не создаётся (файл начинается с контента)

### Requirement: Структура контента — H1 до breadcrumb

Каждый сгенерированный `.md`-файл SHALL иметь следующий порядок секций:

1. YAML frontmatter (если есть `title`)
2. Пустая строка
3. `# {title_ru}` — заголовок H1
4. Пустая строка
5. Breadcrumb-строка (если генерируется)
6. Пустая строка
7. Тело страницы

H1 SHALL быть первым текстовым элементом после frontmatter. Breadcrumb SHALL располагаться после H1.

#### Scenario: Файл открывается на H1

- **WHEN** конвертируется страница с `title_ru = "Глобальный контекст.ВозможностьЧтенияXML"` и breadcrumb активирован
- **THEN** первая не-frontmatter строка файла: `# Глобальный контекст.ВозможностьЧтенияXML`
- **THEN** breadcrumb расположен после H1, отделён пустой строкой

#### Scenario: Страница без breadcrumb — H1 первая строка

- **WHEN** страница не имеет breadcrumb (нет `_index`-pass)
- **THEN** первая строка файла (после frontmatter если есть): `# {title_ru}`


### Requirement: Идемпотентность и логи запуска

Конвертер SHALL поддерживать повторный безопасный запуск через `--clean`. По завершении SHALL создавать в `--out` служебные файлы:

- `_meta.json` — параметры запуска, статистика (всего страниц, сконвертировано, ошибок, обрезанных имён, нерезолвленных ссылок), длительность
- `_truncated.log` — обрезанные имена (orig_path → final_name)
- `_collisions.log` — коллизии после нормализации
- `_unresolved.log` — ссылки на отсутствующие таргеты
- `_errors.log` — ошибки конвертации отдельных страниц (с путём и текстом исключения)

В процессе выполнения конвертер SHALL дополнительно публиковать структурированные runtime-логи в `stdout` в формате `key=value` для наблюдения за текущим состоянием и длительностью этапов.

#### Scenario: Повторный запуск с --clean

- **WHEN** скрипт запущен с `--clean` на ранее использованный `--out`
- **THEN** содержимое `--out` полностью удалено
- **THEN** vault создан заново с нуля
- **THEN** сгенерирован новый `_meta.json`

#### Scenario: Ошибка одной страницы не прерывает остальные

- **WHEN** при конвертации одной из 25 000 страниц возникает исключение
- **THEN** ошибка записана в `_errors.log` (путь страницы + текст исключения)
- **THEN** остальные страницы конвертируются успешно
- **THEN** в `_meta.json.failed` отражено количество ошибок

#### Scenario: Логи этапов доступны агенту в stdout

- **WHEN** запускается конвертация
- **THEN** `stdout` содержит события `event=stage_start` и `event=stage_end` для ключевых этапов
- **THEN** каждое `event=stage_end` содержит `elapsed_sec`

#### Scenario: Прогресс длинной конвертации читается из stdout

- **WHEN** выполняется этап `convert_*` на большом архиве
- **THEN** `stdout` периодически содержит события `event=progress` с полями `done`, `total`, `pct`, `rate_fps`, `eta_sec`
