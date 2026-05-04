## ADDED Requirements

### Requirement: build_archive_index strips English parenthetical before filename derivation

When `build_archive_index()` consumes a raw H1 title from `title_map` (produced by `quick_scan_titles`), it SHALL apply `PAGETITLE_SPLIT_RE` to extract only `group(1)` (the Russian part before the parenthesised English name) before passing the result to `title_to_filename()`. If `PAGETITLE_SPLIT_RE` does not match (no parenthetical), the full title SHALL be used unchanged.

#### Scenario: shcntx page title with English parenthetical produces Russian-only filename

- **WHEN** `quick_scan_titles()` returns `"Задача.Имя_задачи (Task.Имя_задачи)"` for a given path
- **THEN** `build_archive_index()` derives filename `Задача.Имя_задачи.md` (no English suffix)

#### Scenario: shlang page title with English parenthetical produces Russian-only filename

- **WHEN** `quick_scan_titles()` returns `"Если (If)"` for a shlang page
- **THEN** `build_archive_index()` derives filename `lang__Если.md` (no English suffix)

#### Scenario: Title without parenthetical is unchanged

- **WHEN** `quick_scan_titles()` returns `"Глобальный контекст"` (no parenthesised part)
- **THEN** `build_archive_index()` derives filename `Глобальный_контекст.md`
