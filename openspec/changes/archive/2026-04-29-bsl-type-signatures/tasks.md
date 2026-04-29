## 1. Парсер типов из Markdown-тела

- [x] 1.1 Написать функцию `parse_type_tokens(type_line: str) -> list[tuple[str, str]]` — принимает строку после `Тип:`, возвращает список `(name, link_or_empty)` для каждого типа (MD-ссылки и plain-текст)
- [x] 1.2 Написать функцию `render_type_tokens(tokens: list[tuple[str, str]]) -> str` — форматирует токены в `[\`Name\`](link) | [\`Name2\`](link2)` или `` `Name` `` если ссылки нет
- [x] 1.3 Покрыть `parse_type_tokens` юнит-тестами: одиночный тип со ссылкой, составной тип, plain `Произвольный`, trailing spaces/dot

## 2. Определение типа страницы и извлечение структуры

- [x] 2.1 Написать функцию `detect_page_kind(text: str) -> str | None` — возвращает `"method"`, `"property"`, `"ctor"` или `None` по наличию маркеров в Markdown-тексте
- [x] 2.2 Написать функцию `extract_method_signatures(text: str) -> list[str]` — для каждого синтаксического варианта извлекает имя метода, параметры с типами, return-тип; возвращает список отформатированных строк сигнатур
- [x] 2.3 Написать функцию `extract_property_signature(text: str) -> str | None` — извлекает имя свойства и его тип
- [x] 2.4 Покрыть тестами: одновариантный метод, двухвариантный метод, void-метод, свойство с одним типом, свойство с составным типом, страница без распознанного типа

## 3. Вставка сигнатуры в файл

- [x] 3.1 Написать функцию `build_signature_block(text: str) -> str | None` — оркестрирует `detect_page_kind` + `extract_*`; возвращает итоговый блок строк для вставки или `None` если страница пропускается
- [x] 3.2 Написать функцию `inject_signature_into_content(filepath: Path, signature_block: str) -> bool` — вставляет блок после H1+breadcrumb, перед телом; если сигнатура уже есть — заменяет; возвращает `True` если файл изменён
- [x] 3.3 Покрыть тестами: вставка в файл с breadcrumb, вставка в файл без breadcrumb, идемпотентность (повторная вставка не дублирует)

## 4. Новый этап pipeline

- [x] 4.1 Добавить константу `STAGE_INJECT_SIGNATURES = "inject_signatures"` в `convert.py`
- [x] 4.2 Добавить поля `signatures_injected: int` и `signatures_skipped: int` в dataclass `Stats`
- [x] 4.3 Написать функцию `inject_all_signatures(out_dir: Path, index_filenames: set[str], stats: Stats) -> int` — обходит все `.md` кроме index-файлов, вызывает `build_signature_block` + `inject_signature_into_content`
- [x] 4.4 Вызвать `run_stage(STAGE_INJECT_SIGNATURES, inject_all_signatures, ...)` в `main()` после `STAGE_INJECT_BREADCRUMBS`
- [x] 4.5 Убедиться что `stats.signatures_injected` и `stats.signatures_skipped` попадают в `_meta.json`

## 5. Тесты интеграции и регрессия

- [x] 5.1 Добавить тест в `tests/test_parse.py` (или новый `tests/test_signatures.py`): полный round-trip для метода с параметрами → ожидаемая строка сигнатуры в выходном файле
- [x] 5.2 Проверить что существующие тесты (`test_breadcrumbs.py`, `test_toc.py`) не падают после добавления нового этапа
- [x] 5.3 Убедиться что index-файлы (`_index*.md`) не получают сигнатуры
