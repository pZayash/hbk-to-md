"""Тесты нормализации имён файлов."""
from pathlib import Path

import pytest

from convert import (
    LANG_PREFIX,
    archive_path_to_filename,
    build_archive_index,
    disambiguate,
    quick_extract_title,
    quick_scan_titles,
    resolve_parent_title,
    title_to_filename,
    truncate_filename,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_html(root: Path, rel: str, title: str = "") -> None:
    """Create a minimal HTML file with given V8SH_pagetitle at rel path under root."""
    p = root / Path(rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'<html><head><meta charset="utf-8"></head><body>'
        f'<h1 class="V8SH_pagetitle">{title}</h1></body></html>',
        encoding="utf-8",
    )


def test_nested_path():
    src = "objects/Global context/methods/catalog1566/CanReadXML1628.html"
    expected = "objects__Global_context__methods__catalog1566__CanReadXML1628.md"
    assert archive_path_to_filename(src) == expected


def test_top_level_path():
    assert archive_path_to_filename("objects/catalog56.html") == "objects__catalog56.md"


def test_tables_path():
    assert archive_path_to_filename("tables/table10.html") == "tables__table10.md"


def test_lang_prefix():
    assert archive_path_to_filename("def_String", prefix=LANG_PREFIX) == "lang__def_String.md"


def test_lang_prefix_with_html():
    assert archive_path_to_filename("def_String.html", prefix=LANG_PREFIX) == "lang__def_String.md"


def test_cyrillic_in_segment():
    src = "objects/Очень/Длинный/Путь.html"
    assert archive_path_to_filename(src) == "objects__Очень__Длинный__Путь.md"


def test_spaces_replaced_with_underscore():
    assert archive_path_to_filename("a/b c/d e f.html") == "a__b_c__d_e_f.md"


def test_truncation_short_name_unchanged():
    name = "objects__catalog56.md"
    out, was = truncate_filename(name, "objects/catalog56.html")
    assert out == name
    assert was is False


def test_truncation_long_name():
    long_seg = "X" * 250
    name = f"objects__{long_seg}.md"
    out, was = truncate_filename(name, "objects/" + long_seg + ".html")
    assert was is True
    assert len(out) <= 200
    assert out.endswith(".md")
    assert "__TRUNC_" in out


def test_truncation_deterministic_hash():
    long_seg = "Y" * 250
    src = "objects/" + long_seg + ".html"
    name = archive_path_to_filename(src)
    out1, _ = truncate_filename(name, src)
    out2, _ = truncate_filename(name, src)
    assert out1 == out2


def test_disambiguate_no_collision():
    out, was = disambiguate("foo.md", set())
    assert out == "foo.md"
    assert was is False


def test_disambiguate_collision_chain():
    used = {"foo.md"}
    out, was = disambiguate("foo.md", used)
    assert out == "foo-2.md"
    assert was is True
    used.add(out)
    out2, _ = disambiguate("foo.md", used)
    assert out2 == "foo-3.md"


def test_disambiguate_no_extension():
    out, was = disambiguate("bar", {"bar"})
    assert out == "bar-2"
    assert was is True


# ---------- title_to_filename -------------------------------------------

def test_title_to_filename_basic():
    assert title_to_filename("Глобальный контекст.ВозможностьЧтенияXML") == "Глобальный_контекст.ВозможностьЧтенияXML.md"


def test_title_to_filename_simple():
    assert title_to_filename("Глобальный контекст") == "Глобальный_контекст.md"


def test_title_to_filename_lang_prefix():
    assert title_to_filename("Строка", prefix=LANG_PREFIX) == "lang__Строка.md"


def test_title_to_filename_strips_unsafe_chars():
    assert title_to_filename('foo/bar:baz*qux?"<>|') == "foobarbazqux.md"


def test_title_to_filename_strips_leading_trailing_dots_underscores():
    assert title_to_filename("._test_.") == "test.md"


def test_title_to_filename_empty_returns_empty():
    assert title_to_filename("") == ""


def test_title_to_filename_only_unsafe_returns_empty():
    assert title_to_filename('/:*?"<>|') == ""


# ---------- quick_extract_title / quick_scan_titles ----------------------

_SAMPLE_H1_HTML = b"""\
<html><head><meta charset="utf-8"></head><body>
<h1 class="V8SH_pagetitle">\xd0\x93\xd0\xbb\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82.\xd0\x92\xd0\xbe\xd0\xb7\xd0\xbc\xd0\xbe\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c\xd0\xa7\xd1\x82\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8fXML</h1>
</body></html>
"""

_NO_H1_HTML = b"<html><body><p>no heading</p></body></html>"


def test_quick_extract_title_found(tmp_path: Path):
    f = tmp_path / "page.html"
    f.write_bytes(_SAMPLE_H1_HTML)
    title = quick_extract_title(f)
    assert title == "Глобальный контекст.ВозможностьЧтенияXML"


def test_quick_extract_title_decodes_html_entities(tmp_path: Path):
    html = b"<html><body><h1 class=\"V8SH_pagetitle\">&lt;\xd0\x98\xd0\xbc\xd1\x8f\xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82\xd0\xb0&gt;</h1></body></html>"
    f = tmp_path / "page.html"
    f.write_bytes(html)
    title = quick_extract_title(f)
    assert title == "<Имяобъекта>"
    assert "&lt;" not in title


def test_quick_extract_title_missing(tmp_path: Path):
    f = tmp_path / "page.html"
    f.write_bytes(_NO_H1_HTML)
    assert quick_extract_title(f) == ""


def test_quick_scan_titles_keys_are_lowercase(tmp_path: Path):
    (tmp_path / "Page.html").write_bytes(_SAMPLE_H1_HTML)
    result = quick_scan_titles(tmp_path)
    assert "page.html" in result
    assert result["page.html"] == "Глобальный контекст.ВозможностьЧтенияXML"


def test_quick_scan_titles_missing_h1_maps_empty(tmp_path: Path):
    (tmp_path / "noh1.html").write_bytes(_NO_H1_HTML)
    result = quick_scan_titles(tmp_path)
    assert result.get("noh1.html") == ""


# ---------- resolve_parent_title --------------------------------------------

def test_resolve_parent_title_finds_immediate_parent(tmp_path: Path):
    title_map = {
        "tables/table6.html": "Каталог.Имя_справочника (Catalog.Имя_справочника)",
        "tables/table6/fields/ref38.html": "Ссылка (Ref)",
    }
    result = resolve_parent_title("tables/table6/fields/Ref38.html", title_map)
    assert result == "Каталог.Имя_справочника (Catalog.Имя_справочника)"


def test_resolve_parent_title_walks_up_multiple_levels(tmp_path: Path):
    title_map = {
        "tables/catalog63.html": "Корневой",
        "tables/catalog63/table66.html": "Документ.Изменения (Document.Changes)",
    }
    result = resolve_parent_title("tables/catalog63/table66/fields/Ref546.html", title_map)
    assert result == "Документ.Изменения (Document.Changes)"


def test_resolve_parent_title_returns_empty_when_no_ancestor(tmp_path: Path):
    title_map = {"other/page.html": "Другое"}
    result = resolve_parent_title("tables/table6/fields/Ref38.html", title_map)
    assert result == ""


# ---------- build_archive_index — collision resolution ----------------------

def test_build_archive_index_colliding_titles_get_parent_enriched_names(tmp_path: Path):
    _make_html(tmp_path, "tables/table6.html", "Каталог.Имя_справочника (Catalog.Имя_справочника)")
    _make_html(tmp_path, "tables/table6/fields/Ref38.html", "Ссылка (Ref)")
    _make_html(tmp_path, "tables/table81.html", "ВнешнийИсточникДанных.Таблица (ExternalDataSource.Table)")
    _make_html(tmp_path, "tables/table81/fields/Ref645.html", "Ссылка (Ref)")

    title_map = {
        "tables/table6.html": "Каталог.Имя_справочника (Catalog.Имя_справочника)",
        "tables/table6/fields/ref38.html": "Ссылка (Ref)",
        "tables/table81.html": "ВнешнийИсточникДанных.Таблица (ExternalDataSource.Table)",
        "tables/table81/fields/ref645.html": "Ссылка (Ref)",
    }
    index = build_archive_index(tmp_path, prefix="", title_map=title_map)

    name38 = index["tables/table6/fields/ref38.html"]
    name645 = index["tables/table81/fields/ref645.html"]

    assert "Каталог" in name38
    assert "Ссылка" in name38
    assert "ВнешнийИсточникДанных" in name645
    assert "Ссылка" in name645
    assert name38 != name645


def test_build_archive_index_colliding_page_no_parent_falls_back_to_path(tmp_path: Path):
    _make_html(tmp_path, "a/b.html", "Дубль")
    _make_html(tmp_path, "c/d.html", "Дубль")

    title_map = {
        "a/b.html": "Дубль",
        "c/d.html": "Дубль",
    }
    index = build_archive_index(tmp_path, prefix="", title_map=title_map)

    assert index["a/b.html"] == archive_path_to_filename("a/b.html")
    assert index["c/d.html"] == archive_path_to_filename("c/d.html")


def test_build_archive_index_all_unique_values_when_titles_collide(tmp_path: Path):
    _make_html(tmp_path, "tables/table6.html", "Каталог.Х (Catalog.X)")
    _make_html(tmp_path, "tables/table6/fields/Ref38.html", "Ссылка (Ref)")
    _make_html(tmp_path, "tables/table81.html", "ВнешнийИсточникДанных.Т (ExternalDataSource.T)")
    _make_html(tmp_path, "tables/table81/fields/Ref645.html", "Ссылка (Ref)")

    title_map = {
        "tables/table6.html": "Каталог.Х (Catalog.X)",
        "tables/table6/fields/ref38.html": "Ссылка (Ref)",
        "tables/table81.html": "ВнешнийИсточникДанных.Т (ExternalDataSource.T)",
        "tables/table81/fields/ref645.html": "Ссылка (Ref)",
    }
    index = build_archive_index(tmp_path, prefix="", title_map=title_map)
    values = list(index.values())
    assert len(values) == len(set(values))


def test_build_archive_index_non_colliding_pages_unaffected(tmp_path: Path):
    _make_html(tmp_path, "objects/Obj.html", "Глобальный контекст")

    title_map = {"objects/obj.html": "Глобальный контекст"}
    index = build_archive_index(tmp_path, prefix="", title_map=title_map)

    assert index["objects/obj.html"] == title_to_filename("Глобальный контекст")


def test_build_archive_index_title_map_none_uses_path_based_names(tmp_path: Path):
    _make_html(tmp_path, "def_String.html", "Строка (String)")
    _make_html(tmp_path, "def_Number.html", "Число (Number)")

    index = build_archive_index(tmp_path, prefix=LANG_PREFIX, title_map=None)

    assert index["def_string.html"] == archive_path_to_filename("def_String.html", prefix=LANG_PREFIX)
    assert index["def_number.html"] == archive_path_to_filename("def_Number.html", prefix=LANG_PREFIX)


def test_build_archive_index_strips_english_from_lang_title(tmp_path: Path):
    _make_html(tmp_path, "if.html", "Если (If)")
    title_map = {"if.html": "Если (If)"}
    index = build_archive_index(tmp_path, prefix=LANG_PREFIX, title_map=title_map)
    assert index["if.html"] == "lang__Если.md"


def test_build_archive_index_strips_english_from_dotted_title(tmp_path: Path):
    _make_html(tmp_path, "objects/task.html", "Задача.Имя_задачи (Task.Имя_задачи)")
    title_map = {"objects/task.html": "Задача.Имя_задачи (Task.Имя_задачи)"}
    index = build_archive_index(tmp_path, prefix="", title_map=title_map)
    assert index["objects/task.html"] == "Задача.Имя_задачи.md"


def test_build_archive_index_no_parens_title_unchanged(tmp_path: Path):
    _make_html(tmp_path, "objects/obj2.html", "ГлобальныйКонтекст")
    title_map = {"objects/obj2.html": "ГлобальныйКонтекст"}
    index = build_archive_index(tmp_path, prefix="", title_map=title_map)
    assert index["objects/obj2.html"] == "ГлобальныйКонтекст.md"
