"""Тесты нормализации имён файлов."""
from convert import (
    LANG_PREFIX,
    archive_path_to_filename,
    disambiguate,
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
