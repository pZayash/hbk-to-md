## Context

`.hbk` — формат справки 1С. **Это V8 storage container** (та же структура, что у `.cf`/`.epf`/`.erf`), а НЕ просто ZIP-архив с trailer-данными. Изначальное допущение «zipfile читает напрямую» оказалось неверным: `zipfile.BadZipFile: Bad magic number for central directory` на 8.3.25 и 8.3.27 одинаково. Реальная структура (на примере `shcntx_ru.hbk` 8.3.27.1786, ~39 MB):

```text
shcntx_ru.hbk (≈39 MB)
└─ V8 storage (page-based FAT, page=512B)
    ├─ Book                  (доп. метаданные)
    ├─ FileStorage  (≈37 MB) ← это ОБЫЧНЫЙ ZIP с HTML-страницами
    ├─ IndexMainData
    ├─ IndexPackBlock
    ├─ MainData
    ├─ PackBlock
    └─ PackLookup

Распаковка двухступенчатая:
  1. onec_dtools.ContainerReader.extract(deflate=False, recursive=True) → разворачивает V8 storage
  2. zipfile.ZipFile(FileStorage) → разворачивает HTML-страницы

После шага 2:
  objects/                                              166 MB
    __categories__                                      (доступность + min-version)
    catalog{N}.html                                     (страницы разделов)
    catalog{N}/...nested.../{Name|MethodNNNN}.html
    Global context/{events,methods,properties}/...
  tables/                                               4.4 MB
                                                        (типы СКД и др.)

Итого:
  24 980 HTML
  22 285 .st (snippet-фрагменты variant-синтаксиса)
   3 712 __categories__
```

HTML-страницы стандартизованы через CSS-классы:

| Класс | Содержимое |
|---|---|
| `V8SH_pagetitle` | полное имя «Русское (English)» |
| `V8SH_title` | родительский объект |
| `V8SH_heading` | короткое имя метода |
| `V8SH_chapter` | секция: Синтаксис, Параметры, Возвращаемое значение, Описание, Доступность, Пример, Использование в версии |
| `V8SH_rubric` | параметр |
| `V8SH_versionInfo` | версия |

Ссылки внутри HTML двух видов:

1. `v8help://SyntaxHelperContext/objects/X/Y.html` — на файл из того же `shcntx_ru.hbk` (префикс срезается → готовый относительный путь архива)
2. `v8help://SyntaxHelperLanguage/def_String` — на встроенный тип языка из `shlang_ru.hbk`

Внешние ссылки `<a href=http://...?C="id=...">Методическая информация</a>` имеют битый HTML (атрибут без кавычек, значение с кавычками внутри); BeautifulSoup парсит, но в наш output они не нужны.

## Goals / Non-Goals

**Goals**

- Полный 1:1 дамп страниц `shcntx_ru.hbk` + `shlang_ru.hbk` в плоский каталог `.md`-файлов
- Все внутренние ссылки переписаны в относительные markdown-ссылки на соседние `.md` с сохранением якорей `#section`
- Минимальный YAML-frontmatter для Obsidian properties и AI-агентов
- Нулевые внешние бинарные зависимости (только Python + pip)
- Идемпотентность: повторный запуск с `--out` чистит каталог и пересоздаёт

**Non-Goals**

- TOC-парсер `shcntx_root.hbk`
- Семантический парсинг V8SH-классов (V2)
- Иерархия папок в output (плоская раскладка — намеренное решение)
- Распаковка остальных `.hbk` (V2)
- Рендер `.st`-фрагментов

## Decisions

### 1. Stack: Python 3.10+, `onec_dtools` (V8 storage) + stdlib `zipfile`, BeautifulSoup4, markdownify

**Почему**: `.hbk` = V8 storage container (тот же формат, что у `.cf`/`.epf`). Внутри среди прочего файл `FileStorage` — обычный ZIP с HTML. Распаковка двухступенчатая:

1. `onec_dtools.container_reader.ContainerReader(f).extract(out, deflate=False, recursive=True)` — разворачивает V8 storage
2. `zipfile.ZipFile(out / "FileStorage")` — разворачивает HTML-страницы

`onec_dtools` — pip-пакет (16 KB), pure-Python, без бинарей. markdownify даёт качественный HTML→MD; `html2text` отклонён — хуже работает с таблицами.

**Отвергнутые альтернативы:**

- **stdlib `zipfile` напрямую** — изначально предполагалось (как в helpsearch/main.py), но реально не работает: финальный EOCD-record указывает на офсеты внутри страниц V8, не байт файла → `BadZipFile: Bad magic number for central directory`. helpsearch обходит это через subprocess 7z; мы не хотим внешних бинарей.
- **subprocess 7z** — отклонена: требует внешней утилиты в PATH; `onec_dtools` решает то же из pip без бинарей.
- **Свой парсер V8 storage** — отклонена: ~150-200 строк, дублирует `onec_dtools`.

### 2. Плоская раскладка output, иерархия в имени файла

**Почему**: пользователь явно попросил («Иерархия папок плохо для агентов»). Плюсы:
- Агенту проще: один `glob` `*.md`, нет рекурсии
- Уникальность имени гарантируется самим путём архива
- Перенос между vault'ами тривиален

**Схема имени**: путь архива → имя файла:
- разделитель сегментов: `__` (двойное подчёркивание)
- пробелы в сегментах: `_` (одиночное)
- расширение: `.html` → `.md`

Примеры:
```
objects/Global context/methods/catalog1566/CanReadXML1628.html
  → objects__Global_context__methods__catalog1566__CanReadXML1628.md

objects/catalog56.html
  → objects__catalog56.md

tables/table10.html
  → tables__table10.md
```

Для `shlang_ru.hbk` префикс `lang__`:
```
SyntaxHelperLanguage/def_String  →  lang__def_String.md
```

### 3. Лимит длины имени файла

Windows path = 260 символов. С учётом базового пути и префиксов — лимит на имя файла берём 200 символов. Если превышено — обрезка хвоста + хеш SHA1[:8] исходного пути для уникальности:
```
objects__Очень_Длинный_Путь...__Method.md
  → objects__Очень_Длинный_Путь__TRUNC_a3f2c1d9.md
```

Лог обрезанных в `--out/_truncated.log`.

### 4. Переписывание ссылок ДО конвертации в Markdown

Делаем на стадии BeautifulSoup, до `markdownify`. Логика:

```
v8help://SyntaxHelperContext/objects/X/Y.html#anchor
  → ./objects__X__Y.md#anchor

v8help://SyntaxHelperLanguage/def_String
  → ./lang__def_String.md

http(s)://...
  → оставить как есть

href БЕЗ кавычек (битый «Методическая информация»)
  → удалить целиком (BS4 видит как broken attr; убираем тег <a>, оставляем текст)
```

Якорь после `#` сохраняем дословно. Файл-таргет может не существовать (битая ссылка в исходнике или ссылка на `def_X` который не пришёл из shlang) — это **не** ошибка, лог в `--out/_unresolved.log`.

### 5. YAML-frontmatter — минимальный для MVP

```yaml
---
title_ru: "Глобальный контекст.ВозможностьЧтенияXML"
title_en: "Global context.CanReadXML"
source_path: "objects/Global context/methods/catalog1566/CanReadXML1628.html"
hbk_source: "shcntx_ru"        # shcntx_ru | shlang_ru
hbk_version: "8.3.25.1445"     # из CLI-параметра --version
availability: "8.0"            # из <p class="V8SH_versionInfo">, если найдено
---
```

**Почему минимальный**: парсить структуру V8SH-секций (params/returns/availability-list) — V2-задача. Сейчас вытаскиваем только то, что в `<h1 class="V8SH_pagetitle">` (надёжно, всегда есть) и одну строку версии (если есть).

`title_ru/en` из h1: формат `"Русское (English)"` → split по последней паре круглых скобок.

### 6. Конвертация HTML→MD: markdownify

Параметры:
- `strip=['script', 'style']` — удалить технические теги
- `heading_style='ATX'` — `#` вместо `===`
- `bullets='-'` — стандартные маркеры
- ВАЖНО: **не** включать `<a>` в strip (как сделал helpsearch) — мы их уже переписали в нужный вид

Кодировка: HTML внутри hbk заявляет `<meta charset="utf-8">` и реально UTF-8 (BOM встречается). Читаем `utf-8-sig` → fallback `cp1251`.

### 7. CLI

```
python tools/hbk-to-md/convert.py \
    --hbk PATH/shcntx_ru.hbk \
    --lang-hbk PATH/shlang_ru.hbk \
    --out PATH/vault \
    --version 8.3.25.1445 \
    [--clean]
```

- `--lang-hbk` опциональный (но рекомендуется для целостности ссылок)
- `--clean` — снести `--out` целиком перед конвертацией (по умолчанию: ругаться, если не пусто)
- `--version` опциональный, по умолчанию извлекается из имени каталога `bin` (`.../1cv8/8.3.25.1445/bin/...`) или ставится `unknown`

### 8. Идемпотентность и логи

- При `--clean` — `shutil.rmtree(out); mkdir(out)`
- В output создаются служебные файлы:
  - `_meta.json` — параметры запуска, статистика (всего страниц, сконвертировано, обрезано имён, нерезолвленных ссылок)
  - `_truncated.log` — список обрезанных имён (orig_path → final_name)
  - `_unresolved.log` — ссылки на отсутствующие таргеты

### 9. Производительность

24 980 HTML × 2 файла (shcntx + shlang) ≈ 30k страниц. Однопоточный pipeline (read → parse → rewrite → markdownify → write). На SSD оценка 5-15 минут — приемлемо, многопоточность не нужна для MVP.

## Risks / Trade-offs

- **Риск**: коллизия имён после нормализации (например пробелы → `_` дают одинаковые ключи).
  → **Митигация**: при коллизии добавляем суффикс `-N` и логируем в `_collisions.log`.

- **Риск**: ссылки `def_X` из `shlang_ru` перекрываются между разными `.hbk` версиями.
  → V2; в MVP принимаем «победитель — кто пришёл вторым».

- **Риск**: 50k файлов в одной плоской папке тормозят Obsidian/Windows Explorer.
  → Obsidian справляется (тестировано до 100k); Explorer — да, тормозит, но это не наш сценарий.

- **Trade-off**: плоская раскладка ломает обзор «по разделам справки». Принято осознанно ради удобства агентов; раздел можно восстановить из `source_path` во frontmatter, либо в V2 сделать MOC-генератор поверх.

- **Риск**: битый HTML «Методическая информация» — BS4 может неоднозначно его парсить.
  → Используем парсер `lxml` (более снисходительный), и regex-проверка на `href=http...?C="` перед обработкой.

- **Trade-off**: shlang_ru.hbk — отдельный проход. У него другая структура внутри (там `def_*` без иерархии). Конвертер делает раздельные раундтрипы, общий код вынесен.

## Migration Plan

Не применимо (новый отдельный инструмент, не затрагивает существующий код).

## Open Questions

- Куда складывать output по умолчанию? **Решение в MVP**: путь обязательный параметр `--out`, дефолта нет (рекомендация в README: `_forResearch/hbk-vault/` — уже в `.gitignore`).
- Нужна ли версия `8.3.16` совместимости (старые .hbk)? **Статус**: проверено на 8.3.25.1445 и 8.3.27.1786 — обе работают через `onec_dtools`. 8.3.16 не тестировалось (если потребуется — V2).
- Парсинг `.st`-фрагментов (variant-syntax) — **V2**.
- Извлечение специфичных страниц shlang без расширения (`def_String` и т.п.) — **сделано**: content-sniffing по сигнатуре `<HTML`/`<!DOCTYPE` с учётом UTF-8 BOM.
