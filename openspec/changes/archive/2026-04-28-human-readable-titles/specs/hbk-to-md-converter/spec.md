## MODIFIED Requirements

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

## MODIFIED Requirements

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

## MODIFIED Requirements

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
