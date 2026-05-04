## 1. Strip English parenthetical in build_archive_index

- [x] 1.1 In `build_archive_index()`, before calling `title_to_filename(title, ...)`, apply `PAGETITLE_SPLIT_RE` to extract `group(1).strip()` as `ru_title`; use `ru_title` (or full title if no match) as the argument

## 2. Update PRIMITIVE_TYPE_STEMS

- [x] 2.1 Replace `"lang__Булево_(Boolean)"` → `"lang__Булево"` in `PRIMITIVE_TYPE_STEMS`
- [x] 2.2 Replace `"lang__Число_(Number)"` → `"lang__Число"`
- [x] 2.3 Replace `"lang__Строка_(String)"` → `"lang__Строка"`
- [x] 2.4 Replace `"lang__Дата_(Date)"` → `"lang__Дата"`
- [x] 2.5 Replace `"lang__Неопределено_(Undefined)"` → `"lang__Неопределено"`

## 3. Update tests

- [x] 3.1 Update `tests/test_filename.py` scenarios that assert filenames containing `_(English)` to expect Russian-only names
- [x] 3.2 Add test: `build_archive_index` with title `"Если (If)"` → filename `lang__Если.md`
- [x] 3.3 Add test: `build_archive_index` with title `"Задача.Имя_задачи (Task.Имя_задачи)"` → filename `Задача.Имя_задачи.md`
- [x] 3.4 Add test: title without parenthetical → filename unchanged

## 4. Verify

- [x] 4.1 Run full test suite (`pytest`) — all tests pass
- [x] 4.2 Spot-check generated vault: confirm `lang__Если.md`, `lang__Булево.md` exist; confirm no `_(` in any `.md` filename
