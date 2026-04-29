## MODIFIED Requirements

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
