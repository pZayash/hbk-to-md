"""Тесты BSL-сигнатур."""
from pathlib import Path

import pytest

from signatures import (
    build_signature_block,
    detect_page_kind,
    extract_method_signatures,
    extract_property_signature,
    inject_signature_into_content,
    is_primitive,
    parse_type_tokens,
    render_type_tokens,
)


# ── 1.3 parse_type_tokens ────────────────────────────────────────────────────

def test_parse_type_tokens_single_link():
    tokens = parse_type_tokens("[Строка](lang__def_String.md).")
    assert tokens == [("Строка", "lang__def_String.md")]


def test_parse_type_tokens_compound():
    tokens = parse_type_tokens(
        "[Поток](Поток_(Stream).md), [ПотокВПамяти](ПотокВПамяти_(MemoryStream).md), "
        "[ФайловыйПоток](ФайловыйПоток_(FileStream).md)."
    )
    assert tokens == [
        ("Поток", "Поток_(Stream).md"),
        ("ПотокВПамяти", "ПотокВПамяти_(MemoryStream).md"),
        ("ФайловыйПоток", "ФайловыйПоток_(FileStream).md"),
    ]


def test_parse_type_tokens_plain():
    tokens = parse_type_tokens("Произвольный")
    assert tokens == [("Произвольный", "")]


def test_parse_type_tokens_trailing_spaces_dot():
    tokens = parse_type_tokens("[Строка](lang__def_String.md).   ")
    assert tokens == [("Строка", "lang__def_String.md")]


# ── render_type_tokens ────────────────────────────────────────────────────────

def test_render_type_tokens_with_link():
    # primitive → no link emitted
    assert render_type_tokens([("Строка", "lang__def_String.md")]) == "`Строка`"


def test_render_type_tokens_non_primitive_link():
    assert render_type_tokens([("Поток", "Поток_(Stream).md")]) == "[`Поток`](Поток_(Stream).md)"


def test_render_type_tokens_compound():
    result = render_type_tokens([
        ("Поток", "Поток_(Stream).md"),
        ("Неопределено", "lang__def_Undefined.md"),
    ])
    # lang__def_Undefined is primitive → plain text; Поток is not → link kept
    assert result == "[`Поток`](Поток_(Stream).md) | `Неопределено`"


def test_render_type_tokens_plain():
    assert render_type_tokens([("Произвольный", "")]) == "`Произвольный`"


def test_is_primitive_hardcoded_stem():
    assert is_primitive("lang__def_String.md") is True
    assert is_primitive("lang__Булево_(Boolean).md") is True


def test_is_primitive_prefix_pattern():
    assert is_primitive("lang__def_SomeNewType.md") is True


def test_is_primitive_non_primitive():
    assert is_primitive("Поток_(Stream).md") is False
    assert is_primitive("objects__Global_context.md") is False


# ── 2.4 detect_page_kind ─────────────────────────────────────────────────────

_SIMPLE_METHOD = """\
# Объект.Метод

**↑** breadcrumb

Объект (Object)

Метод (Method)

Синтаксис:

Метод(<Параметр>)

Параметры:

<Параметр> (обязательный)

Тип: [Строка](link).

Возвращаемое значение:

Тип: [Массив](link).

Описание:

Описание метода.
"""

_VOID_METHOD = """\
# Объект.Метод

**↑** breadcrumb

Синтаксис:

Метод(<Параметр>)

Параметры:

<Параметр> (обязательный)

Тип: [Строка](link).

Описание:

Описание метода.
"""

_CTOR = """\
# Объект.По умолчанию

**↑** breadcrumb

Синтаксис:

Новый Объект(<Параметр>)

Параметры:

<Параметр> (обязательный)

Тип: [Строка](link).

Описание:

Создаёт объект.
"""

_PROPERTY = """\
# Объект.Свойство

**↑** breadcrumb

Объект (Object)

Свойство (Property)

Использование:

Только чтение.

Описание:

Тип: [Строка](link).
Описание свойства.
"""

_COMPOUND_PROPERTY = """\
# Объект.Свойство2

**↑** breadcrumb

Использование:

Только чтение.

Описание:

Тип: [ТипА](link1), [Неопределено](link2).
"""

_TWO_VARIANT_METHOD = """\
# Объект.Метод

**↑** breadcrumb

Вариант синтаксиса: Вариант 1

Синтаксис:

Метод(<А>)

Параметры:

<А> (обязательный)

Тип: [Строка](link).

Описание варианта метода:

Описание.

Вариант синтаксиса: Вариант 2

Синтаксис:

Метод(<Б>, <В>)

Параметры:

<Б> (обязательный)

Тип: [Число](link2).

<В> (необязательный)

Тип: [Булево](link3).

Описание варианта метода:

Описание.
"""

_NO_KIND = """\
# Раздел

**↑** breadcrumb

Обычная страница без синтаксиса и типов.
"""


def test_detect_page_kind_method():
    assert detect_page_kind(_SIMPLE_METHOD) == "method"


def test_detect_page_kind_ctor():
    assert detect_page_kind(_CTOR) == "ctor"


def test_detect_page_kind_property():
    assert detect_page_kind(_PROPERTY) == "property"


def test_detect_page_kind_none():
    assert detect_page_kind(_NO_KIND) is None


# ── extract_method_signatures ─────────────────────────────────────────────────

def test_extract_method_single_variant():
    sigs = extract_method_signatures(_SIMPLE_METHOD)
    assert len(sigs) == 1
    assert sigs[0] == "`Метод`(`<Параметр>`: [`Строка`](link)) → [`Массив`](link)"


def test_extract_method_void():
    sigs = extract_method_signatures(_VOID_METHOD)
    assert len(sigs) == 1
    assert sigs[0] == "`Метод`(`<Параметр>`: [`Строка`](link))"
    assert "→" not in sigs[0]


def test_extract_method_two_variants():
    sigs = extract_method_signatures(_TWO_VARIANT_METHOD)
    assert len(sigs) == 2
    assert sigs[0] == "`Метод`(`<А>`: [`Строка`](link))"
    assert sigs[1] == "`Метод`(`<Б>`: [`Число`](link2), `<В>`: [`Булево`](link3))"


def test_extract_method_no_params():
    text = """\
# Объект.Метод

Синтаксис:

Метод()

Описание:

Текст.
"""
    sigs = extract_method_signatures(text)
    assert len(sigs) == 1
    assert sigs[0] == "`Метод`()"


# ── extract_property_signature ────────────────────────────────────────────────

def test_extract_property_single_type():
    sig = extract_property_signature(_PROPERTY)
    assert sig == "`Свойство`: [`Строка`](link)"


def test_extract_property_compound_type():
    sig = extract_property_signature(_COMPOUND_PROPERTY)
    assert sig == "`Свойство2`: [`ТипА`](link1) | [`Неопределено`](link2)"


def test_extract_property_no_type():
    text = "# Объект.Свойство\n\nНет типа.\n"
    assert extract_property_signature(text) is None


# ── build_signature_block ─────────────────────────────────────────────────────

def test_build_signature_block_method():
    block = build_signature_block(_SIMPLE_METHOD)
    assert block == "`Метод`(`<Параметр>`: [`Строка`](link)) → [`Массив`](link)"


def test_build_signature_block_two_variants():
    block = build_signature_block(_TWO_VARIANT_METHOD)
    assert block is not None
    lines = block.split("\n\n")
    assert len(lines) == 2


def test_build_signature_block_none():
    assert build_signature_block(_NO_KIND) is None


# ── 3.3 inject_signature_into_content ────────────────────────────────────────

def test_inject_with_breadcrumb(tmp_path: Path):
    f = tmp_path / "page.md"
    f.write_text(
        "# Заголовок\n\n**↑** [Главная](_index.md)\n\nТело страницы.\n",
        encoding="utf-8",
    )
    changed = inject_signature_into_content(f, "`Метод`()")
    assert changed is True
    text = f.read_text(encoding="utf-8")
    assert "**↑** [Главная](_index.md)\n\n<!-- signature:start -->\n`Метод`()\n<!-- signature:end -->\n\nТело страницы." in text


def test_inject_without_breadcrumb(tmp_path: Path):
    f = tmp_path / "page.md"
    f.write_text("# Заголовок\n\nТело страницы.\n", encoding="utf-8")
    changed = inject_signature_into_content(f, "`Метод`()")
    assert changed is True
    text = f.read_text(encoding="utf-8")
    assert "# Заголовок\n\n<!-- signature:start -->\n`Метод`()\n<!-- signature:end -->\n\nТело страницы." in text


def test_inject_idempotent(tmp_path: Path):
    f = tmp_path / "page.md"
    f.write_text(
        "# Заголовок\n\n**↑** [Главная](_index.md)\n\n<!-- signature:start -->\n`Метод`()\n<!-- signature:end -->\n\nТело страницы.\n",
        encoding="utf-8",
    )
    original = f.read_text(encoding="utf-8")
    changed = inject_signature_into_content(f, "`Метод`()")
    assert changed is False
    assert f.read_text(encoding="utf-8") == original


def test_inject_replaces_existing(tmp_path: Path):
    f = tmp_path / "page.md"
    f.write_text(
        "# Заголовок\n\n**↑** [Главная](_index.md)\n\n<!-- signature:start -->\n`СтараяСигнатура`()\n<!-- signature:end -->\n\nТело.\n",
        encoding="utf-8",
    )
    changed = inject_signature_into_content(f, "`НоваяСигнатура`()")
    assert changed is True
    text = f.read_text(encoding="utf-8")
    assert "`НоваяСигнатура`()" in text
    assert "`СтараяСигнатура`()" not in text


# ── 5.1 Round-trip: method page → expected signature in output ────────────────

def test_round_trip_method_in_file(tmp_path: Path):
    content = _SIMPLE_METHOD
    f = tmp_path / "test.md"
    f.write_text(content, encoding="utf-8")

    block = build_signature_block(content)
    assert block is not None
    inject_signature_into_content(f, block)

    result = f.read_text(encoding="utf-8")
    expected_sig = "`Метод`(`<Параметр>`: [`Строка`](link)) → [`Массив`](link)"
    assert expected_sig in result
    # Signature appears after breadcrumb
    bc_pos = result.index("**↑**")
    sig_pos = result.index(expected_sig)
    assert sig_pos > bc_pos


# ── 5.3 Index files are not modified ─────────────────────────────────────────

def test_index_file_no_signature(tmp_path: Path):
    from convert import INDEX_PREFIX
    from signatures import build_signature_block

    index_content = f"# Root Index\n\n**↑** breadcrumb\n\nSome content.\n"
    f = tmp_path / f"{INDEX_PREFIX}.md"
    f.write_text(index_content, encoding="utf-8")

    # inject_all_signatures skips index files; verify build_signature_block returns None for them
    # (index files lack Синтаксис/Тип/Использование markers)
    assert build_signature_block(index_content) is None
