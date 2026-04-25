## ADDED Requirements

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
