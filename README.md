# hbk-to-md

CLI-конвертер `.hbk` (1С:Предприятие) -> плоский каталог `.md` для Obsidian, индексирования и AI/RAG-пайплайнов.

`hbk-to-md` извлекает страницы из `shcntx_ru.hbk` (и опционально `shlang_ru.hbk`), конвертирует HTML в Markdown, переписывает внутренние `v8help://`-ссылки и добавляет навигационный слой (`_index*.md` + breadcrumbs).

## Возможности

- Конвертация `.hbk` в плоскую структуру Markdown-файлов
- YAML frontmatter с метаданными (заголовки, версия, источник, доступность)
- Нормализация и дедупликация имён файлов с логами коллизий/усечений
- Переписывание `v8help://`-ссылок в относительные `.md`-ссылки
- Генерация индексов `_index*.md` и breadcrumbs для удобной навигации
- Технические отчёты о прогоне (`_meta.json`, `_unresolved.log`, `_errors.log`, ...)

## Установка

```bash
python -m pip install -r requirements.txt
```

Требуется Python ≥ 3.10. Внешние утилиты (`7z`, `V8unpack`) не нужны — `.hbk` разворачивается двухступенчато pip-пакетом `onec_dtools` (V8 storage container) + stdlib `zipfile` (внутренний `FileStorage` = обычный ZIP с HTML-страницами).

## Запуск

```bash
python convert.py \
    --hbk "C:/Program Files/1cv8/8.3.25.1445/bin/shcntx_ru.hbk" \
    --lang-hbk "C:/Program Files/1cv8/8.3.25.1445/bin/shlang_ru.hbk" \
    --out _forResearch/hbk-vault \
    --clean
```

Параметры:

- `--hbk PATH` — основной архив `shcntx_ru.hbk` (обязательный)
- `--lang-hbk PATH` — архив встроенного языка `shlang_ru.hbk` (рекомендуется для целостности ссылок)
- `--out PATH` — выходной каталог (обязательный, дефолта нет)
- `--version X.Y.Z.W` — версия платформы; если не передана, выводится из родительского пути `.../1cv8/X.Y.Z.W/bin/...`
- `--clean` — снести `--out` целиком перед конвертацией (по умолчанию: ругаться, если каталог не пуст)

## Формат выходных файлов

Каждая HTML-страница архива → один `.md` в корне `--out`. Иерархия архива закодирована в имени:

```text
objects/Global context/methods/catalog1566/CanReadXML1628.html
  → objects__Global_context__methods__catalog1566__CanReadXML1628.md
```

Правила нормализации имени:

- разделитель сегментов: `__` (двойное подчёркивание)
- пробелы внутри сегмента: `_` (одиночное)
- расширение: `.html` → `.md`
- страницы из `shlang_ru.hbk` получают префикс `lang__`
- имя > 200 символов: хвост обрезается, добавляется `__TRUNC_<sha1[:8]>`, лог в `_truncated.log`
- коллизии: суффикс `-2`, `-3`, …, лог в `_collisions.log`

## Навигация

После конвертации дополнительно генерируется слой навигации:

- корневой файл `_index.md` — точка входа во vault
- файловые индексы `_index__<prefix>.md` для внутренних узлов иерархии
- breadcrumb-строка на каждой content-странице под frontmatter

### `_index*.md`

- `_index.md` содержит общую статистику и ссылки на top-level разделы (`objects`, `lang`, `tables`)
- `_index__<prefix>.md` содержит:
  - frontmatter `type: index`, `source_prefix`, `parent_index`
  - H1 с названием раздела
  - ссылку на парную content-страницу (если она есть)
  - секции `## Подразделы (N)` и/или `## Страницы (N)`
  - counts в ссылках на подразделы (число страниц в поддереве)
- для больших списков (>50) включается алфавитная группировка с подзаголовками `### А`, `### Б`, ...

### Breadcrumb на страницах

Каждая content-страница получает строку вида:

```text
**↑** [Главная](_index.md) › [Объекты](_index__objects.md) › [Глобальный контекст](objects__Global_context.md) › ...
```

- строка вставляется сразу после frontmatter и перед H1
- текущая страница в breadcrumb не включается (последний элемент — родитель)
- если для сегмента нет ни content-страницы, ни `_index__...`, сегмент пропускается

### Как скрыть `_index*.md` в Obsidian (опционально)

Если нужен только контент без технических index-файлов, добавьте в `.obsidianignore`:

```text
_index*.md
```

### YAML-frontmatter

Каждый `.md` начинается с блока:

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

Поля:

- `title_ru` / `title_en` — из `<h1 class="V8SH_pagetitle">` («Русское (English)»); `title_en` пустая, если скобок нет
- `source_path` — относительный путь файла внутри `.hbk`-архива
- `hbk_source` — `shcntx_ru` или `shlang_ru`
- `hbk_version` — версия платформы 1С
- `availability` — минимальная версия из `<p class="V8SH_versionInfo">`, если найдена; иначе поле отсутствует

### Переписывание ссылок

Внутренние `v8help://...` → относительные markdown-ссылки на соседние `.md`:

```text
v8help://SyntaxHelperContext/objects/X/Y.html#anchor   →  [Title](objects__X__Y.md#anchor)
v8help://SyntaxHelperLanguage/def_String                →  [Строка](lang__def_String.md)
http(s)://...                                            →  без изменений
```

Битые `<a href=http://...?C="..."` (без кавычек на href) — тег удаляется, остаётся только текст.

### Служебные файлы в `--out`

| Файл | Содержимое |
| --- | --- |
| `_meta.json` | параметры запуска, статистика (включая `index_files_generated` и `breadcrumbs_added`), длительность |
| `_truncated.log` | обрезанные имена (orig_path → final_name) |
| `_collisions.log` | коллизии после нормализации |
| `_unresolved.log` | ссылки на отсутствующие таргеты |
| `_errors.log` | ошибки конвертации отдельных страниц |

## Известные ограничения

- Нет TOC из `shcntx_root.hbk` — иерархия восстанавливается только из `source_path`
- Нет рендера `.st`-фрагментов (variant-синтаксис)
- Нет семантического парсинга V8SH-классов (params/returns/types) — V2-задача
- Конвертируются только `shcntx_ru.hbk` + `shlang_ru.hbk`; остальные `.hbk` (`v8cnthlp`, `1cv8_*`, `adm*_ru`) — V2

## Тесты

```bash
python -m pytest tests/
```
