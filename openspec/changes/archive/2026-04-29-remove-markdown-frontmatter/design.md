## Context

Текущий output-формат содержит YAML frontmatter в content-файлах и в `_index*.md`. Это усложняет чтение людьми и увеличивает token-cost при работе с Markdown как с основным артефактом. При этом навигация (`_index`, breadcrumbs, inline TOC) уже реализована в теле документов и может работать без frontmatter.

Изменение затрагивает несколько участков пайплайна: генерацию content-файлов, генерацию index-файлов, insertion breadcrumbs, тесты формата и README.

## Goals / Non-Goals

**Goals:**
- Полностью убрать YAML frontmatter из всех итоговых `.md` файлов.
- Сохранить человекочитаемую структуру и навигацию (H1, breadcrumbs, TOC/листинги) без потери UX.
- Сохранить технические метаданные в `_meta.json`, не возвращая их в Markdown.
- Обновить спецификацию, тесты и документацию до единого контракта.

**Non-Goals:**
- Не менять алгоритмы извлечения title, rewrite ссылок, построения иерархии и имён файлов.
- Не менять формат служебных логов (`_errors.log`, `_unresolved.log`, `_meta.json` и т.д.).
- Не добавлять новый формат метаданных в markdown-теле (например, HTML-комментарии или custom блоки).

## Decisions

### 1) Удалить frontmatter для content-файлов полностью

**Decision:** перестать генерировать frontmatter в `convert_one()`/`build_frontmatter()`, content-файл начинается с H1 (или с тела, если H1 отсутствует).

**Why:** это напрямую снижает шум и token-cost, а заголовок и breadcrumb остаются в явном виде.

**Alternative considered:** оставить минимальный `title:`.  
**Rejected:** всё равно создаёт служебный префикс в каждом файле и противоречит цели “никаких Obsidian properties”.

### 2) Удалить frontmatter для `_index.md` и `_index__*.md`

**Decision:** `render_root_index()` и `render_index()` формируют только markdown-тело без `--- ... ---`.

**Why:** index-файлы тоже читаются людьми и входят в контекстные выборки; единый формат без frontmatter упрощает восприятие.

**Alternative considered:** оставить технический frontmatter только у index-файлов.  
**Rejected:** нарушает единообразие и частично сохраняет исходную проблему.

### 3) Унифицировать вставку breadcrumb под формат без frontmatter

**Decision:** `inject_breadcrumb_into_content()` опирается на H1-first логику; ветка frontmatter не является обязательной.

**Why:** после удаления frontmatter код проще, меньше ветвлений и edge-case поведения.

**Alternative considered:** оставить dual-режим (с/без frontmatter) для обратной совместимости.  
**Rejected:** лишняя сложность без практической необходимости для нового контракта.

### 4) Закрепить breaking-change в специке и README

**Decision:** явным текстом указать, что downstream-интеграции не должны читать YAML из `.md`; источник технических данных — `_meta.json`.

**Why:** предотвращает неявные регрессии и задаёт правильный путь миграции.

## Risks / Trade-offs

- **[Risk] Внешние скрипты читают YAML из `.md`** → **Mitigation:** явный breaking-change note в proposal/spec/README + указание миграции на `_meta.json`.
- **[Risk] Регресс в вставке breadcrumb после удаления ветки frontmatter** → **Mitigation:** обновить и расширить тесты `test_breadcrumbs.py` на H1/no-H1 сценарии.
- **[Risk] Несогласованность документации и тестов** → **Mitigation:** менять spec/tests/README в одном change, не частями.
- **[Trade-off] Потеря “машинной” метки `type` в index markdown** → **Mitigation:** использовать имя файла (`_index*.md`) и `_meta.json` как источники классификации.
