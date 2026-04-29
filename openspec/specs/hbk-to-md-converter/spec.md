## Purpose

Define behavior of the HBK to Markdown conversion pipeline and vault output format.

## Requirements


### Requirement: CLI-конвертер `.hbk` → плоский каталог `.md`

Система SHALL предоставлять Python-скрипт `convert.py`, который принимает путь к `shcntx_ru.hbk` и (опционально) `shlang_ru.hbk` и записывает в указанный выходной каталог набор Markdown-файлов — по одному на каждую HTML-страницу справки.

Конвертер SHALL поддерживать флаг `--breadcrumbs` (по умолчанию отсутствует). Когда флаг не передан, этап `STAGE_INJECT_BREADCRUMBS` SHALL быть полностью пропущен. Когда флаг передан, этап выполняется с форматом HTML-анкоров для предков (см. capability `graph-friendly-breadcrumbs`).

#### Scenario: Базовый запуск с одним архивом

- **WHEN** вызван `python convert.py --hbk PATH/shcntx_ru.hbk --out PATH/vault --clean`
- **THEN** в `PATH/vault/` создан набор `.md`-файлов — по одному на каждую HTML-страницу из `shcntx_ru.hbk`
- **THEN** в `PATH/vault/_meta.json` записаны параметры запуска и статистика конвертации
- **THEN** хлебные крошки НЕ инжектированы (флаг `--breadcrumbs` не передан)

#### Scenario: Запуск с обоими архивами

- **WHEN** вызван `python convert.py --hbk shcntx_ru.hbk --lang-hbk shlang_ru.hbk --out vault --clean`
- **THEN** в `vault/` присутствуют файлы из обоих архивов; страницы из `shlang_ru.hbk` имеют префикс `lang__`

#### Scenario: Отказ при непустом выходном каталоге без --clean

- **WHEN** `--out` указывает на непустой каталог и `--clean` не передан
- **THEN** скрипт завершается с ненулевым кодом и сообщением об ошибке
- **THEN** файлы в `--out` не модифицируются

#### Scenario: Флаг --breadcrumbs включает инжекцию

- **WHEN** вызван `python convert.py --hbk ... --out ... --clean --breadcrumbs`
- **THEN** этап `STAGE_INJECT_BREADCRUMBS` выполняется
- **THEN** в каждую страницу инжектирована строка хлебных крошек в формате HTML-анкоров для предков

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

Итоговые Markdown-файлы SHALL НЕ содержать YAML-frontmatter. Ни content-файлы, ни `_index.md`, ни `_index__*.md` НЕ MUST начинаться с блока `--- ... ---`.

#### Scenario: Content-файл без frontmatter
- **WHEN** конвертируется страница с заголовком `Глобальный контекст.ВозможностьЧтенияXML`
- **THEN** итоговый `.md` не содержит стартовый блок `--- ... ---`
- **THEN** файл начинается с `# Глобальный контекст.ВозможностьЧтенияXML` (или с тела, если H1 отсутствует)

#### Scenario: Index-файл без frontmatter
- **WHEN** генерируется `_index.md` и `_index__Объекты.md`
- **THEN** в начале файлов отсутствует YAML-блок `--- ... ---`
- **THEN** файлы содержат только markdown-контент и навигационные секции

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

### Requirement: Корневой `_index.md` как точка входа в vault

Конвертер SHALL генерировать в корне `--out` файл `_index.md` как human-readable точку входа в vault. Файл SHALL содержать H1 с версией платформы 1С, статистику по количеству страниц и список ссылок на top-секции (`objects`, `lang`, `tables`) — без YAML-frontmatter.

#### Scenario: Базовая генерация `_index.md`
- **WHEN** конвертация завершена и в vault есть страницы из `shcntx_ru.hbk` (24 500) и `shlang_ru.hbk` (1 042)
- **THEN** в `--out/_index.md` есть H1 с версией платформы
- **THEN** в теле есть строка статистики `Всего страниц: **25 542**`
- **THEN** в теле есть секция `## Разделы` со ссылками на top-level index-файлы
- **THEN** файл не содержит frontmatter-полей `type`, `hbk_version`, `total_pages`

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

Каждый `_index__<prefix>.md` SHALL содержать заголовок H1 с title, опциональную ссылку на парную content-страницу (если есть) и листинг direct children в двух группах: подразделы и страницы. YAML-frontmatter (`type`, `source_prefix`, `parent_index`) SHALL NOT записываться в файл.

#### Scenario: Листинг подразделов и страниц
- **WHEN** под префиксом `objects/Global context` есть 3 sub-папки (`events`, `methods`, `properties`) и 0 leaf-страниц
- **THEN** в `_index__objects__Global_context.md` есть секция `## Подразделы (3)` со ссылками на соответствующие target-файлы
- **THEN** секции `## Страницы` нет
- **THEN** файл не содержит frontmatter `type: index`, `source_prefix`, `parent_index`

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

После основной конвертации каждая content-страница (`objects__*.md`, `lang__*.md`, `tables__*.md`) SHALL получить breadcrumb-блок после H1, перед телом страницы, отделённый пустой строкой. Формат breadcrumb: `**↑** [Главная](_index.md) › <segment1> › <segment2> › ...`.

Walk родителей по `source_path`: для каждого префикса (от корня до родителя текущей страницы) SHALL резолвиться таргет:

1. Если есть content-страница для префикса (lookup в архивном индексе) → линк на неё с `title_ru` как text
2. Иначе если есть `_index__<prefix>.md` → линк на `_index` с resolved title (см. отдельное требование)
3. Иначе segment SHALL пропускаться (skip)

Корневой элемент `[Главная](_index.md)` всегда присутствует. Текущая страница (последний segment) НЕ включается в breadcrumb (она видна как H1 ниже).

#### Scenario: Breadcrumb для глубокой страницы со всеми резолвами
- **WHEN** конвертируется `objects/Global context/methods/catalog1566/CanReadXML1628.html`
- **THEN** в `objects__...__CanReadXML1628.md` первая строка — H1 текущей страницы
- **THEN** breadcrumb расположен сразу после H1 и одной пустой строки
- **THEN** между breadcrumb и телом страницы одна пустая строка

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

Итоговые `.md`-файлы SHALL полностью исключать YAML-frontmatter для token-optimized выгрузки. Запрещены как "полные" поля (`title_ru`, `title_en`, `source_path`, `hbk_source`, `hbk_version`, `availability`), так и "минимальные" (`title`, `type`, `source_prefix`, `parent_index`, `total_pages`).

#### Scenario: Ни один `.md` не содержит YAML frontmatter
- **WHEN** конвертация завершена
- **THEN** любой output-файл с расширением `.md` не начинается с `---`
- **THEN** технические метаданные доступны через `_meta.json`, а не через frontmatter

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

### Requirement: Этап STAGE_INJECT_SIGNATURES в pipeline

Конвертер SHALL выполнять этап `STAGE_INJECT_SIGNATURES` после `STAGE_INJECT_BREADCRUMBS` и до `STAGE_WRITE_LOGS`. Этап SHALL обходить все content-файлы vault и вставлять BSL-сигнатуры согласно capability `bsl-type-signatures`.

#### Scenario: Этап присутствует в stdout-логах
- **WHEN** конвертация запущена
- **THEN** `stdout` содержит события `event=stage_start stage=inject_signatures` и `event=stage_end stage=inject_signatures elapsed_sec=...`

#### Scenario: Этап выполняется после breadcrumbs
- **WHEN** конвертация завершена
- **THEN** в каждом vault content-файле breadcrumb расположен до сигнатуры (порядок: H1 → breadcrumb → сигнатура → тело)

### Requirement: Позиция сигнатуры в структуре content-файла

Сигнатура SHALL вставляться строго после H1 и breadcrumb-строки, перед первым контентным блоком тела страницы. Порядок секций в content-файле SHALL быть:

1. `# Заголовок`
2. Пустая строка
3. Breadcrumb-строка (если есть)
4. Пустая строка
5. Строка(и) BSL-сигнатуры
6. Пустая строка
7. Тело страницы

#### Scenario: Сигнатура расположена после breadcrumb
- **WHEN** content-файл содержит H1, breadcrumb и BSL-сигнатуру
- **THEN** порядок в файле: H1 → пустая строка → breadcrumb → пустая строка → сигнатура → пустая строка → тело
