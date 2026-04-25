## Why

Vault `_forResearch/hbk-vault/` (25 542 страницы) — плоская куча `.md` без точки входа и без обратной навигации. Пользователь, открыв конкретную страницу справки, не видит, к какому разделу/классу она принадлежит и как добраться до родителя. Список файлов в Obsidian/файловом менеджере не даёт обзора иерархии — имена закодированы через `__`, но визуально не группируются. Нужен (а) каталог-указатель `_index.md` с навигацией по разделам и (б) хлебные крошки на каждой странице — путь от корня к текущей.

## What Changes

- Расширить `tools/hbk-to-md/convert.py` двумя пост-процессорами после основной конвертации:
  - **TOC-генератор** — multi-level: один `_index.md` в корне vault'а + по одному `_index__<prefix>.md` для каждого внутреннего узла иерархии (уровней `objects/`, `objects/Global context/`, `objects/Global context/methods/` и т.д.). Имя стартует с `_index__` чтобы не пересекаться с реальными страницами `objects__...`. Каждый `_index` содержит листинг direct-children (с линками на content-страницы и/или вложенные `_index`).
  - **Breadcrumb-генератор** — добавляет наверх каждой content-страницы (под frontmatter, перед H1) блок вида `**↑** [Главная](_index.md) › [Объекты](_index__objects.md) › [Глобальный контекст](objects__Global_context.md) › ...`. Источник иерархии — `source_path` из frontmatter. Сегменты без content-`.md` И без `_index_*.md` пропускаются (skip).
- Решения по развилкам (defaults — могут быть пересмотрены в design):
  - **B-pure**: `_index` и content-страницы — отдельные файлы; section-страницы НЕ мутируются content'ом
  - **Title для _index**: копируется `title_ru` из парной section .md, если есть; иначе fallback на имя сегмента (`events` → "События", `methods` → "Методы", `properties` → "Свойства", иначе raw segment)
  - **Алфавитная группировка** в _index — при `N children > 50`
  - **Counts** `(N страниц)` рядом с каждой подгруппой
  - **Сортировка** в _index: сначала sub-sections (узлы с детьми) по `title_ru`, потом leaves по `title_ru`
- Расширить `tools/hbk-to-md/README.md`: описание формата `_index*.md`, breadcrumb-блока, правил skip
- Добавить юнит-тесты:
  - `test_toc.py` — построение дерева из source_paths, разбиение на `_index` файлы, alphabetical-grouping threshold
  - `test_breadcrumbs.py` — walk segments, skip пустых, формат markdown-линка
- Дополнить `_meta.json` статистикой: `index_files_generated`, `breadcrumbs_added`

### Revision: Token-Optimized Output

В рамках этой же change вносятся уточнения формата вывода для агентов:

- Убрать избыточные `_index__<prefix>.md` для узлов, у которых есть парная content-страница `objects__...`/`tables__...`/`lang__...`.
- Для таких узлов оглавление (листинг direct children) встраивать прямо в content-страницу после основного содержания.
- Оставить только необходимые `_index`-файлы:
  - `_index.md` (корень),
  - `_index__<prefix>.md` только для узлов без собственной content-страницы.
- Удалять из markdown итоговые блоки/ссылки на `Методическая информация`.
- Минимизировать frontmatter: убрать `title_ru`, `title_en`, `source_path`, `hbk_source`, `hbk_version`, `availability` из output `.md` (метаданные остаются в `_meta.json` и во внутренних структурах pipeline при необходимости).

## Capabilities

### New Capabilities

<!-- TOC + breadcrumbs — расширение существующего capability hbk-to-md-converter, не отдельная capability -->

### Modified Capabilities

- `hbk-to-md-converter`: добавляются требования к TOC (`_index*.md`) и breadcrumbs в content-страницах

## Impact

- **Изменения в `tools/hbk-to-md/convert.py`**: пост-обработка vault'а после основной конвертации; +2 модуля (TOC builder, breadcrumb injector)
- **Vault output**: появляется ~500-700 новых `_index__*.md` файлов; каждая из 25 542 content-страниц получает 1 строку breadcrumb наверху
- **Идемпотентность**: `--clean` чистит весь vault — TOC и breadcrumbs пересоздаются с нуля
- **Производительность**: оценка +5-15s на пост-обработку (один проход по индексу + один проход по страницам); на фоне основных 405s — не значимо
- **Внешние зависимости**: новых нет (только stdlib + уже существующие BS4/markdownify не нужны для пост-процессинга)
- **Документация**: обновить README.md и AGENTS.md (упомянуть TOC/breadcrumbs)

## Артефакты

- [[design]]
- [[tasks]]
- [[specs/hbk-to-md-converter/spec]]
