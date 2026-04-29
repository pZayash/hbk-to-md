## ADDED Requirements

### Requirement: Этап STAGE_INJECT_SIGNATURES в pipeline
Конвертер SHALL выполнять этап `STAGE_INJECT_SIGNATURES` после `STAGE_INJECT_BREADCRUMBS` и до `STAGE_WRITE_LOGS`. Этап SHALL обходить все content-файлы vault и вставлять BSL-сигнатуры согласно capability `bsl-type-signatures`.

#### Scenario: Этап присутствует в stdout-логах
- **WHEN** конвертация запущена
- **THEN** `stdout` содержит события `event=stage_start stage=inject_signatures` и `event=stage_end stage=inject_signatures elapsed_sec=...`

#### Scenario: Этап выполняется после breadcrumbs
- **WHEN** конвертация завершена
- **THEN** в каждом vault content-файле breadcrumb расположен до сигнатуры (порядок: H1 → breadcrumb → сигнатура → тело)

### Requirement: Позиция сигнатуры в структуре content-файла
Сигнатура SHALL вставляться строго после H1 и breadcrumb-строки, перед первым контентным блоком тела страницы. Порядок секций в content-файле SHALL быть:

1. `# Заголовок`
2. Пустая строка
3. Breadcrumb-строка (если есть)
4. Пустая строка
5. Строка(и) BSL-сигнатуры
6. Пустая строка
7. Тело страницы

#### Scenario: Сигнатура расположена после breadcrumb
- **WHEN** content-файл содержит H1, breadcrumb и BSL-сигнатуру
- **THEN** порядок в файле: H1 → пустая строка → breadcrumb → пустая строка → сигнатура → пустая строка → тело
