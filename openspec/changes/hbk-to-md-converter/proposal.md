## Why

Файлы справки 1С (`*.hbk`) недоступны для индексации `qmd` и для чтения ИИ-агентами без распаковки и конвертации. Платформенная UI-справка из конфигуратора неудобна для агентов: нет full-text поиска, нет векторного индекса, нет прямого чтения файлов. Существующие OSS-конвертеры либо делают **структурный** экспорт (только методы/типы — `alkoleft/platform-context-exporter`), либо парсят `.hbk` без записи на диск (`Antonio1C/1c-syntax-helper-mcp` → Elasticsearch). Нет инструмента, который выдаёт **полный дамп страниц** в плоский набор `.md`-файлов, пригодный одновременно для Obsidian и для индексации `qmd`.

## What Changes

- Добавить Python-конвертер `tools/hbk-to-md/convert.py` (CLI), который:
  - Распаковывает `shcntx_ru.hbk` и `shlang_ru.hbk` через `zipfile` (стандарт. либа, V8-trailer игнорится автоматически)
  - Парсит каждый HTML через BeautifulSoup, конвертит в Markdown через `markdownify`
  - Перезаписывает ссылки `v8help://SyntaxHelperContext/...` и `v8help://SyntaxHelperLanguage/...` в относительные `[title](path.md)` с сохранением якорей `#section`
  - Складывает все `.md` **плоско** в один выходной каталог, иерархия исходного архива отражается в имени файла через разделитель `__`
  - Добавляет YAML-frontmatter: `title_ru`, `title_en`, `source_path`, `hbk_version`, `availability`
- Добавить `tools/hbk-to-md/requirements.txt` (beautifulsoup4, markdownify, lxml)
- Добавить `tools/hbk-to-md/README.md` — кратко: установка, запуск, формат output

## Non-Goals (V2)

- TOC-парсер `shcntx_root.hbk` (бренд-иерархия 1С)
- Семантический парсинг V8SH-классов (структурный экспорт параметров/типов в frontmatter)
- Конвертация остальных `.hbk` (`v8cnthlp`, `1cv8_*`, `adm*_ru`)
- Иерархия папок в output
- Рендер `.st`-фрагментов (variant-синтаксис)
- MCP-сервер поверх vault (Obsidian + qmd уже умеют)

## Capabilities

### New Capabilities

- `hbk-to-md-converter`: CLI-конвертер `.hbk` → плоский набор `.md` для Obsidian и `qmd`-индексации

### Modified Capabilities

<!-- Изменений требований к существующим спекам нет -->

## Артефакты

- [[design]]
- [[tasks]]
- [[specs/hbk-to-md-converter/spec]]

## Impact

- Новый каталог `tools/hbk-to-md/`:
  - `convert.py` — CLI-конвертер
  - `requirements.txt` — зависимости (beautifulsoup4, markdownify, lxml)
  - `README.md` — usage
- Output (вне репозитория, путь задаётся параметром `--out`): по умолчанию `_forResearch/hbk-vault/` или путь, указанный пользователем; в репозиторий **не коммитится** (≈25 000 файлов, ~150 MB) — добавить в `.gitignore` если по умолчанию пишется внутрь репо
- `.gitignore` — добавить запись по умолчанию для output-каталога
- Зависимости только Python ≥3.10 + три pip-пакета; `7z` не требуется
