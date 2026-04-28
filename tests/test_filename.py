"""Тесты нормализации имён файлов."""
from pathlib import Path

import pytest

from convert import (
    LANG_PREFIX,
    archive_path_to_filename,
    disambiguate,
    quick_extract_title,
    quick_scan_titles,
    title_to_filename,
    truncate_filename,
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
