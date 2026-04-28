## Context

Vault `_forResearch/hbk-vault/` после конвертации содержит:

```text
25 542 страницы .md
   2 служебных файла (_meta.json, _unresolved.log)

Глубина (число __ сегментов в имени):
  2 сегм:    63   objects__Global_context, lang__def_String, tables__table10
  3 сегм:   296   objects__Global_context__events, ...
  4 сегм:  2076
  5 сегм:  2385
  6 сегм: 15573   ← bulk
  7 сегм:  5064
  8 сегм:    85

Top-level: objects/, tables/, lang/  (нет .md для этих корней)
Section pages СУЩЕСТВУЮТ для большинства промежуточных уровней:
  objects__catalog1649.md           → "Интерфейс"
  objects__catalog1649__catalog1890.md → "Форма клиентского приложения"
  objects__Global_context.md         → "Глобальный контекст"

Дыры — некоторые промежуточные уровни не имеют своей .md:
  objects/Global context/methods/   ← нет .md, только folder
  objects/Global context/properties/
  objects/Global context/events/
  objects/                          ← top, нет .md
  tables/, lang/                    ← аналогично
```

Каждая страница имеет frontmatter с `source_path` (полный путь в архиве), `title_ru`, `title_en`, `hbk_source`. Этого достаточно для построения дерева — без обращения к `shcntx_root.hbk`.

Существующий конвертер: `tools/hbk-to-md/convert.py` (~470 строк), pipeline `extract → parse → rewrite → markdownify → write`. Пост-обработка не предусмотрена.

## Goals / Non-Goals

**Goals:**

- `_index.md` в корне vault'а как точка входа со списком top-секций и краткой статистикой
- `_index__<prefix>.md` для каждого внутреннего узла иерархии — листинг direct children с линками
- Breadcrumb-блок наверху каждой content-страницы (под frontmatter, перед H1) — кликабельный путь от `_index.md` к текущей странице
- Иерархия восстанавливается из `source_path` (без зависимости от `_root.hbk`)
- Идемпотентность: `--clean` пересоздаёт всё с нуля
- Не мутировать content существующих страниц (только добавить breadcrumb-строку наверху)

**Non-Goals:**

- Парсинг `shcntx_root.hbk` (V2; текущая иерархия из `source_path` достаточна)
- Изменение содержимого section-страниц (B-pure, не B-merge)
- Полнотекстовый поиск/индекс в `_index` (Obsidian + qmd для этого)
- MOC-подход (Map of Contents с авторскими описаниями) — только автогенерация
- Вложенные/раскрывающиеся (`<details>`) блоки в `_index` — плоский список с алфавитной группировкой

## Decisions

### 1. Архитектура: post-processing pass после основной конвертации

После того как `_convert_archive` отработал для shcntx и shlang, выполняем 2 прохода:

```text
Pass 1: build_hierarchy()
  - Пройти все .md в out/ (или использовать накопленный archive_index)
  - Построить tree: {prefix: TreeNode(children=[...], page=Optional[filename], title=str)}
  - prefix = source_path без расширения, в нижнем регистре

Pass 2a: write_index_files(tree)
  - Для каждого internal node — сгенерировать _index__<prefix>.md
  - Корневой _index.md — особый: статистика + 3 топ-секции

Pass 2b: inject_breadcrumbs(tree)
  - Для каждой content-страницы — re-read, вставить breadcrumb-блок после frontmatter, write обратно
```

**Альтернатива (отвергнута)**: генерация breadcrumb сразу в `convert_one` (inline). Минус — на момент конверсии страницы X дерево ещё не построено (mы не знаем title парных section-страниц). Можно обойти двухпроходно — но post-process чище разделяет обязанности.

### 2. Имя `_index*.md` файлов: префикс `_index__`

```text
_index.md                                               (root)
_index__objects.md                                       (для objects/)
_index__objects__Global_context.md                       (для objects/Global context/)
_index__objects__Global_context__methods.md              (для methods/)
_index__objects__catalog1649.md                          (для catalog1649/ — есть и content-страница objects__catalog1649.md рядом)
_index__lang.md
_index__tables.md
```

Префикс `_index__` отделён от content-имён двойным `__`. Реальные content-имена начинаются с `objects__`/`lang__`/`tables__` — коллизий нет. Сортировка в файловом менеджере: все `_index*` группируются вместе после `_collisions.log`/`_errors.log` и перед content-файлами.

**Сортировка root-файлов:**

```text
_collisions.log
_errors.log
_index.md                          ← root TOC
_index__lang.md
_index__objects.md
_index__objects__Global_context.md
... ~700 _index__... файлов
_index__tables.md
_meta.json
_truncated.log
_unresolved.log
lang__def_Boolean.md
... 25 542 content
```

**Альтернативы (отвергнуто):**

- `__index.md` (с двойным `_`): визуально странно
- `0_index.md` (с цифрой): теряется `_`-семантика «служебный»
- Переименовать логи в `_log_*` чтобы `_index.md` сортировался первым: лишняя инвазивность; user явно отказался от усложнения

### 3. Когда генерировать `_index` для узла

Правило: для каждого **internal** node (узла, у которого есть хотя бы один child). Leaf-страницы (без children) не получают `_index`.

```text
objects/Global context/methods/catalog1566/CanReadXML1628.html   → leaf, нет _index
objects/Global context/methods/catalog1566/                       → есть children, есть _index
objects/Global context/methods/                                   → есть children, есть _index (даже без content .md)
objects/Global context/                                           → есть children, есть _index (parallel с content .md)
objects/                                                          → есть children, есть _index (top, нет content .md)
ROOT                                                              → _index.md (особый)
```

Оценка: **~700 `_index*.md` файлов** (количество internal node в дереве).

### 4. Содержимое `_index__<prefix>.md`

```markdown
---
type: index
source_prefix: "objects/Global context"
parent_index: "_index__objects.md"
---
# Глобальный контекст

[Содержание страницы раздела →](objects__Global_context.md)

> *Описание раздела см. на странице [Глобальный контекст](objects__Global_context.md).*

## Подразделы (3)

- [События (12)](_index__objects__Global_context__events.md)
- [Методы (1547)](_index__objects__Global_context__methods.md)
- [Свойства (203)](_index__objects__Global_context__properties.md)

---

**↑** [Главная](_index.md) › [Объекты](_index__objects.md)
```

Для leaf-`_index` (нет под-узлов с детьми, только список content-страниц):

```markdown
---
type: index
source_prefix: "objects/Global context/methods/catalog1566"
parent_index: "_index__objects__Global_context__methods.md"
---
# Группа методов работы с XML

[Содержание страницы раздела →](objects__Global_context__methods__catalog1566.md)

## Страницы (4)

- [ВозможностьЧтенияXML (CanReadXML)](objects__Global_context__methods__catalog1566__CanReadXML1628.md)
- [НачатьЧтениеXML (BeginReadXML)](...)
- [ОкончаниеЧтенияXML (EndReadXML)](...)
- [ПрочитатьXML (ReadXML)](...)

---

**↑** [Главная](_index.md) › [Объекты](_index__objects.md) › [Глобальный контекст](objects__Global_context.md) › [Методы](_index__objects__Global_context__methods.md)
```

### 5. Корневой `_index.md`

```markdown
---
type: index-root
hbk_version: "8.3.27.1786"
total_pages: 25542
---
# Vault: 1С:Предприятие 8.3.27.1786 — справка

Всего страниц: **25 542** (shcntx_ru: 24 500, shlang_ru: 1 042)

## Разделы

- [Объекты (24 500 страниц)](_index__objects.md)
  Все классы платформы, методы, свойства, события
- [Встроенный язык (1 042)](_index__lang.md)
  Типы данных и литералы языка 1С
- [Таблицы](_index__tables.md)
  Системные таблицы (СКД и др.)
```

### 6. Алфавитная группировка при N > 50

```markdown
## Страницы (1547)

### А

- [АбсолютноеЗначение (Abs)](...)

### В

- [ВводЗначения (InputValue)](...)

### ...
```

Группировка по первой букве `title_ru`. Для смешанных русско/латинских имён используем `title_ru` (всегда заполнено для shcntx).

### 7. Сортировка children в `_index`

Двухуровневая:

1. Сначала **подразделы** (узлы с детьми) — секция `## Подразделы (N)`, отсортированы по `title_ru`
2. Потом **страницы** (leaf-страницы) — секция `## Страницы (N)`, отсортированы по `title_ru`

Если только подразделы — секции `Страницы` нет. И наоборот. Если N > 50 в секции `Страницы` — алфавитная группировка внутри.

### 8. Title для `_index` без парной content-страницы

Для папок без своей .md (например, `methods/`, `properties/`, `events/`):

```python
SEGMENT_TITLES = {
    "methods": "Методы",
    "properties": "Свойства",
    "events": "События",
    "ctors": "Конструкторы",
    "objects": "Объекты",
    "tables": "Таблицы",
    "Global context": "Глобальный контекст",
}
```

Для неизвестных segment'ов — использовать сегмент as-is (например, `catalog1649` без парной — маловероятно, но fallback есть).

### 9. Breadcrumb: формат и место

**Место:** строго после frontmatter, перед H1, отделён пустой строкой:

```markdown
---
title_ru: "..."
...
---
**↑** [Главная](_index.md) › [Объекты](_index__objects.md) › [Глобальный контекст](objects__Global_context.md) › [Методы](_index__objects__Global_context__methods.md) › [Группа методов](objects__Global_context__methods__catalog1566.md)

# Глобальный контекст.ВозможностьЧтенияXML
```

**Resolve targets** для каждого сегмента walk-вверх:

1. Пытаемся найти content `.md` для префикса (lookup в `archive_index`) — приоритетный таргет
2. Иначе — `_index__<prefix>.md` (если такой есть)
3. Иначе — **skip сегмент целиком** (per user decision)

**Корневой:** всегда `[Главная](_index.md)`. Текущая страница — НЕ линк, просто отсутствует в breadcrumb (пользователь видит её как H1 ниже).

**Разделитель:** ` › ` (U+203A) — стандарт для breadcrumb.

### 10. Идемпотентность

- При `--clean` — `prepare_output` уже сносит весь vault → новые `_index` и breadcrumbs создаются с нуля
- Без `--clean` — повторный запуск пересоздаёт `_index` (overwrite), но breadcrumbs могут дублироваться, если страница уже содержит вставленный блок. **Решение:** перед вставкой проверять, есть ли строка `**↑** [Главная]` в начале body — если есть, заменять; иначе вставлять. Регексп `r'^\*\*↑\*\* \[Главная\].*?\n\n'` (multiline, single line block).

Лучше: всегда требовать `--clean` для повторного запуска (уже текущая семантика). Тогда breadcrumb-defensive-replace опционален.

### 11. Производительность

Оценка:

- Pass 1 (build hierarchy): один проход по 25 542 frontmatter'ам ≈ 1-2s
- Pass 2a (write _index): запись ~700 файлов по ~50-1500 строк ≈ 1-3s
- Pass 2b (inject breadcrumbs): re-read + write 25 542 файлов ≈ 5-10s

Итого +10-15s к 405s основной конвертации. Приемлемо, многопоточность не нужна.

**Альтернатива (если медленно)**: вместо re-read content-файлов — буферизовать body в памяти на этапе `convert_one` и записывать только после построения дерева. Это меняет архитектуру (откладывает write всех страниц на конец). Не делаем для MVP.

## Risks / Trade-offs

- **Risk**: ~700 `_index*.md` файлов → засоряют список файлов в Obsidian.
  → **Mitigation**: префикс `_index__` группирует их вместе, легко скрыть в Obsidian через `.obsidianignore` (опционально документируем в README).

- **Risk**: дублирование информации между content section-page и `_index` для того же префикса.
  → **Trade-off**: B-pure — принимаем, content страница описывает РАЗДЕЛ, `_index` — НАВИГАЦИЯ. Линкуем взаимно.

- **Risk**: при добавлении breadcrumb наверх страницы регексп вставки может зацепить лишнее.
  → **Mitigation**: вставка после строки `^---$` (закрытие frontmatter) + before H1. Строгий поиск, тесты на edge cases (страница без frontmatter, страница без H1).

- **Risk**: skip пустых сегментов скрывает иерархию.
  → **Trade-off**: за этот вариант явно проголосовал user. Если получится визуально неудобно — можно V2 переключить на «plain text для пустых».

- **Risk**: breadcrumb для очень глубоких страниц (8 сегментов) занимает 2-3 строки.
  → **Mitigation**: терпимо, Markdown переносит. Альтернатива — обрезать середину "...", но это убивает кликабельность.

- **Trade-off**: TOC из `source_path` ≠ официальный TOC из `_root.hbk`. Может отличаться по группировке/иерархии. Принимается, V2 — переключиться на `_root.hbk`.

- **Trade-off**: алфавитная группировка по `title_ru` смешивает кириллицу и латиницу непредсказуемо в shlang (`def_String` имеет `title_ru` = "Строка"). Решается тем, что shlang-уровень flat (всё под `lang/`), там одна группа.

## Migration Plan

Не применимо (расширение существующего инструмента, не затрагивает прод).

Откат: убрать post-processing pass из `convert.py` или `--no-toc` / `--no-breadcrumbs` CLI-флаги (опционально).

## Open Questions

- Нужен ли CLI-флаг `--no-toc` / `--no-breadcrumbs` для отключения? **MVP: не нужен** (всегда генерим). Если пользователь захочет — добавить позже.
- Сортировка алфавитной группировки: ru-locale или ASCII? **MVP: `str.casefold()` + дефолтная локаль Python** (даёт А-Я кириллицу первой, потом A-Z). Для shcntx все title_ru на русском — порядок будет А→Я.
- Для shlang `lang__def_*` имеет смысл свой `_index__lang.md` со списком ~1000 типов? **MVP: да**, единый файл с алфавитной группировкой (1000 / 30 букв ≈ 33 типа на букву — читаемо).
- Breadcrumb на самих `_index*.md` — нужен? **MVP: да**, в конце блока (как показано в примерах) — навигация вверх между _index файлами.

## Revision: Token-Optimized Rendering

### R1. Не создавать `_index` для узла с парной content-страницей

Ранее модель была B-pure (content + `_index` параллельно). В revision переходим к B-embedded:

- если у узла есть `content_filename`, отдельный `_index__<prefix>.md` НЕ создаётся;
- список дочерних элементов рендерится в самой content-странице после основного текста;
- `_index__<prefix>.md` остаются только для узлов без content-страницы.

Ожидаемый эффект: заметно меньше файлов и меньше дублирования токенов.

### R2. Встраивание оглавления в content-страницу

Для страниц-разделов добавляется блок:

```markdown
## Оглавление

### Подразделы (N)
- ...

### Страницы (M)
- ...
```

Блок вставляется после основного контента страницы (перед финальными служебными ссылками/хвостом).

### R3. Удаление «Методическая информация»

При пост-обработке удаляются:

- отдельная строка `Методическая информация`,
- markdown-ссылка на `http://www.1centerprise.com/devlinks?...` с этим текстом.

Цель: сокращение бесполезного для агента шума в нижней части страниц.

### R4. Минимальный frontmatter

Frontmatter в итоговых `.md` убирается целиком (или оставляется пустым без полей) для снижения токенов.  
Для pipeline-внутренних нужд метаданные остаются в памяти и в `_meta.json`.

### R5. Совместимость breadcrumbs

Breadcrumb продолжает работать без frontmatter:

- источник префикса — внутренний `pages_meta`, собранный во время конвертации;
- при повторной записи content-файла breadcrumb вставляется перед первым `# ` заголовком, если frontmatter отсутствует.
