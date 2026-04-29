## Why

Текущий YAML frontmatter в итоговых `.md` (включая content и `_index*.md`) не несет достаточной ценности для читателя, но увеличивает размер документов, расход токенов и визуальный шум. Нужно перейти к human-first формату, где Markdown-файл содержит только читаемый контент и навигацию.

## What Changes

- Удалить генерацию YAML frontmatter из всех content-файлов (`objects__*.md`, `lang__*.md`, `tables__*.md`).
- Удалить YAML frontmatter из индексов (`_index.md` и `_index__*.md`).
- Сохранить структуру навигации (H1, breadcrumb, TOC/списки разделов) в чистом Markdown без блока `--- ... ---`.
- Обновить тесты и документацию под новый формат вывода.
- **BREAKING**: любые внешние интеграции, которые читали метаданные из frontmatter, должны перейти на `_meta.json` или парсинг тела Markdown.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `hbk-to-md-converter`: требования к формату выходных Markdown-файлов меняются; YAML frontmatter полностью удаляется из всех `.md`.

## Impact

- Затронуты `convert.py` (генерация Markdown, индексов и breadcrumb insertion), тесты `tests/test_parse.py`, `tests/test_breadcrumbs.py`, `tests/test_toc.py`, а также `README.md`.
- Изменяется контракт выходного формата файлов для downstream-скриптов.
