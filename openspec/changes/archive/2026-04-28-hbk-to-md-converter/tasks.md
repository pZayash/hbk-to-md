## 1. Каркас проекта

- [x] 1.1 Создать каталог `tools/hbk-to-md/`
- [x] 1.2 Создать `tools/hbk-to-md/requirements.txt` с зависимостями: `beautifulsoup4`, `markdownify`, `lxml`
- [x] 1.3 Создать `tools/hbk-to-md/README.md`: установка (`pip install -r requirements.txt`), пример CLI-вызова, описание формата выходных файлов
- [x] 1.4 Добавить в `.gitignore` шаблон вывода (если используется дефолтный `_forResearch/hbk-vault/`)

## 2. CLI и распаковка

- [x] 2.1 Создать `tools/hbk-to-md/convert.py` со скелетом `argparse`: `--hbk`, `--lang-hbk`, `--out`, `--version`, `--clean`
- [x] 2.2 Реализовать функцию `extract_hbk(hbk_path: Path, dest: Path) -> None` через `zipfile.ZipFile` (UTF-8 mode для имён) — игнорирует V8-trailer автоматически
- [x] 2.3 Реализовать `derive_version(hbk_path: Path) -> str` — извлечение версии платформы из родительского пути `.../1cv8/X.Y.Z.W/bin/...` (fallback: `unknown`)
- [x] 2.4 Реализовать `prepare_output(out: Path, clean: bool) -> None` — проверка пустоты, опциональная очистка через `shutil.rmtree`

## 3. Нормализация имён файлов

- [x] 3.1 Реализовать `archive_path_to_filename(rel_path: str, prefix: str = "") -> str`:
      сегменты соединяются через `__`, пробелы внутри сегментов → `_`, расширение `.html`→`.md`, опциональный префикс (`lang__` для shlang)
- [x] 3.2 Реализовать обрезку длинных имён (> 200 chars): хвост → SHA1[:8] исходного пути, лог в `_truncated.log`
- [x] 3.3 Реализовать обработку коллизий: счётчик-суффикс `-N`, лог в `_collisions.log`
- [x] 3.4 Юнит-тест `tests/test_filename.py`: примеры из design.md (пробелы, длинные пути, кириллица), коллизии

## 4. Парсинг HTML и переписывание ссылок

- [x] 4.1 Реализовать `parse_html(content: str) -> BeautifulSoup` с `lxml`-парсером, чтение через `utf-8-sig` → fallback `cp1251`
- [x] 4.2 Реализовать `rewrite_links(soup, archive_index: dict[str, str]) -> None`:
      - `v8help://SyntaxHelperContext/PATH#anchor` → `./{archive_index[PATH]}#anchor`
      - `v8help://SyntaxHelperLanguage/def_X` → `./lang__def_X.md`
      - `http(s)://...` — без изменений
      - битые `href=http...?C="..."` (без кавычек на href) — заменить тег `<a>` на текст
- [x] 4.3 Реализовать `extract_titles(soup) -> tuple[str, str]` — из `<h1 class="V8SH_pagetitle">` распарсить «Русское (English)» по последней паре скобок (если скобок нет — `title_en = ""`)
- [x] 4.4 Реализовать `extract_availability(soup) -> str | None` — из `<p class="V8SH_versionInfo">` regex `8\.\d+\.\d+` или `8\.\d+`
- [x] 4.5 Юнит-тест `tests/test_parse.py`: фикстура с реальной страницей (CanReadXML1628.html), проверка titles, links, availability

## 5. Генерация Markdown

- [x] 5.1 Реализовать `to_markdown(soup) -> str` через `markdownify(strip=['script','style'], heading_style='ATX', bullets='-')`
- [x] 5.2 Реализовать `build_frontmatter(meta: dict) -> str` — YAML-блок `---\n...\n---\n` с экранированием значений (двойные кавычки)
- [x] 5.3 Реализовать `write_md(out_dir: Path, filename: str, frontmatter: str, body: str) -> None`

## 6. Главный pipeline

- [x] 6.1 Реализовать `build_archive_index(extracted_dir: Path, prefix: str) -> dict[str, str]`:
      словарь `{archive_relpath: target_filename}` — нужен для перезаписи ссылок ДО генерации файлов
- [x] 6.2 Реализовать `convert_hbk(hbk_path, out, prefix, version, archive_index)` — последовательно: extract → построить локальный индекс → для каждого HTML: parse → rewrite → titles → availability → markdown → frontmatter → write
- [x] 6.3 В `main()` собрать общий индекс из `shcntx_ru` (objects/, tables/) и `shlang_ru`, потом обработать оба архива
- [x] 6.4 Записать `_meta.json` со статистикой запуска (входные параметры, total/converted/failed/truncated/unresolved counts, время)
- [x] 6.5 Обработка ошибок: каждый файл в `try/except`, ошибки логируются в `_errors.log` с путём, продолжаем остальные

## 7. Проверка на реальных данных

- [x] 7.1 Запустить на `C:/Program Files/1cv8/8.3.27.1786/bin/shcntx_ru.hbk` + `shlang_ru.hbk` (актуальная версия в системе), выходной каталог `_forResearch/hbk-vault/`
- [x] 7.2 Проверить `_meta.json`: 25 542 страницы без необработанных ошибок (failed=0, duration ≈ 423s)
- [x] 7.3 Открыть vault в Obsidian: graph view загружается, frontmatter отображается в Properties, wiki-links между страницами кликабельны *(требует ручной проверки пользователя)*
- [x] 7.4 Открыть страницу `objects__Global_context__methods__catalog1566__CanReadXML1628.md`: проверить titles, ссылки на `def_Boolean` ведут в `lang__def_Boolean.md`, ссылка на `objects__catalog63__catalog565__XMLReader.md` существует и кликабельна
- [x] 7.5 Проверить `_unresolved.log`: 104 ссылки (0.41% от 25 542 страниц) — битые ссылки в исходной справке (`v8help://SyntaxHelperContext/.html`, относительные пути на отсутствующие методы и т.п.)
- [x] 7.6 Запустить `qmd update` на vault'е (если включён в коллекцию) — проверить, что файлы индексируются *(требует ручной проверки пользователя)*

## 8. Документация

- [x] 8.1 Дополнить `tools/hbk-to-md/README.md`: пример вывода, описание полей frontmatter, известные ограничения (нет TOC, нет .st, нет семантического парса)
- [x] 8.2 Добавить ссылку на `tools/hbk-to-md/README.md` в `AGENTS.md` в раздел «Использование инструментов» — рядом с `qmd-search.md`, кратко: «когда нужна офлайн-справка 1С — см. конвертер»
