"""Тесты парсинга HTML и переписывания ссылок."""
from convert import (
    LANG_PREFIX,
    extract_availability,
    extract_titles,
    parse_html,
    rewrite_links,
    PRIMITIVE_TYPE_STEMS,
)


SAMPLE_METHOD = """\
<html><head><meta charset="utf-8"><title>x</title></head><body>
<h1 class="V8SH_pagetitle">Глобальный контекст.ВозможностьЧтенияXML (Global context.CanReadXML)</h1>
<p class="V8SH_chapter">Синтаксис:</p>
<p>ВозможностьЧтенияXML(&lt;XMLReader&gt;)</p>
<p class="V8SH_chapter">Параметры:</p>
<p>&lt;XMLReader&gt; (обязательный) Тип:
  <a href="v8help://SyntaxHelperContext/objects/catalog63/catalog565/XMLReader.html">ЧтениеXML</a>.
</p>
<p class="V8SH_chapter">Возвращаемое значение:</p>
<p>Тип: <a href="v8help://SyntaxHelperLanguage/def_Boolean">Булево</a>.</p>
<p class="V8SH_chapter">Доступность:</p>
<p class="V8SH_versionInfo">Версия 8.0</p>
<p>Внешний: <a href="https://example.com">site</a></p>
<p>Битый: <a href=http://www.1centerprise.com/devlinks?C="id=00058O00056;lan=ru" target="_blank">Методическая информация</a></p>
</body></html>
"""

NO_PAREN = """\
<html><body>
<h1 class="V8SH_pagetitle">ПростоеИмяБезСкобок</h1>
</body></html>
"""

NO_VERSION = """\
<html><body>
<h1 class="V8SH_pagetitle">X (Y)</h1>
<p>no versionInfo here</p>
</body></html>
"""


def test_extract_titles_with_parens():
    soup = parse_html(SAMPLE_METHOD)
    ru, en = extract_titles(soup)
    assert ru == "Глобальный контекст.ВозможностьЧтенияXML"
    assert en == "Global context.CanReadXML"


def test_extract_titles_without_parens():
    soup = parse_html(NO_PAREN)
    ru, en = extract_titles(soup)
    assert ru == "ПростоеИмяБезСкобок"
    assert en == ""


def test_extract_availability_found():
    soup = parse_html(SAMPLE_METHOD)
    assert extract_availability(soup) == "8.0"


def test_extract_availability_missing():
    soup = parse_html(NO_VERSION)
    assert extract_availability(soup) is None


def test_rewrite_links_context():
    soup = parse_html(SAMPLE_METHOD)
    archive_index = {
        "objects/catalog63/catalog565/xmlreader.html": "objects__catalog63__catalog565__XMLReader.md",
        "def_boolean": "lang__def_Boolean.md",
    }
    unresolved: list = []
    rewrite_links(soup, archive_index, unresolved, "objects/x/y.html")
    hrefs = [a.get("href") for a in soup.find_all("a")]
    assert "objects__catalog63__catalog565__XMLReader.md" in hrefs
    # lang__def_Boolean is a primitive type — link stripped, plain text "Булево" kept
    assert "lang__def_Boolean.md" not in hrefs
    assert soup.get_text(separator=" ").find("Булево") >= 0
    assert "https://example.com" in hrefs
    assert unresolved == []


def test_rewrite_links_primitive_type_stripped():
    html = '<a href="v8help://SyntaxHelperLanguage/def_String">Строка</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    archive_index = {"def_string": "lang__def_String.md"}
    rewrite_links(soup, archive_index, [], "p.html")
    # link replaced with plain text, no <a> tag remaining
    assert soup.find("a") is None
    assert "Строка" in soup.get_text()


def test_rewrite_links_anchor_preserved():
    html = '<a href="v8help://SyntaxHelperContext/objects/X/Y.html#anchor">T</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    archive_index = {"objects/x/y.html": "objects__X__Y.md"}
    rewrite_links(soup, archive_index, [], "p")
    assert soup.find("a")["href"] == "objects__X__Y.md#anchor"


def test_rewrite_links_unresolved_stripped():
    html = '<a href="v8help://SyntaxHelperContext/objects/missing/Z.html">T</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    unresolved: list = []
    rewrite_links(soup, {}, unresolved, "page.html")
    assert soup.find("a") is None
    assert "T" in soup.get_text()
    assert len(unresolved) == 1


def test_rewrite_links_degenerate_v8help_stripped():
    html = '<a href="v8help://SyntaxHelperContext/.html">x</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    unresolved: list = []
    rewrite_links(soup, {}, unresolved, "page.html")
    assert soup.find("a") is None
    assert len(unresolved) == 1


def test_rewrite_links_double_slash_normalized():
    html = (
        '<a href="v8help://SyntaxHelperContext/objects/catalog63/catalog565/'
        'XMLStringProcessingManager//DeleteDisallowedXMLCharacters6255.html">x</a>'
    )
    soup = parse_html("<html><body>" + html + "</body></html>")
    archive_index = {
        "objects/catalog63/catalog565/xmlstringprocessingmanager/"
        "deletedisallowedxmlcharacters6255.html": "Менеджер.md",
    }
    unresolved: list = []
    rewrite_links(soup, archive_index, unresolved, "page.html")
    assert soup.find("a")["href"] == "Менеджер.md"
    assert unresolved == []


def test_rewrite_links_relative_unresolved_stripped():
    html = '<a href="missing.html">x</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    unresolved: list = []
    rewrite_links(soup, {}, unresolved, "objects/page.html")
    assert soup.find("a") is None
    assert len(unresolved) == 1
    html = '<a href="ExternalDataProcessorsManager/methods/Connect3978.html">Подключить</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    archive_index = {
        "objects/catalog125/catalog224/externaldataprocessorsmanager/methods/connect3978.html":
            "objects__catalog125__catalog224__ExternalDataProcessorsManager__methods__Connect3978.md",
    }
    unresolved: list = []
    rewrite_links(
        soup, archive_index, unresolved,
        "objects/catalog125/catalog224/ExternalDataProcessorsManager.html",
    )
    assert soup.find("a")["href"] == (
        "objects__catalog125__catalog224__ExternalDataProcessorsManager__methods__Connect3978.md"
    )
    assert unresolved == []


def test_rewrite_links_relative_with_anchor():
    html = '<a href="sibling.html#sect">x</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    archive_index = {"objects/sibling.html": "objects__sibling.md"}
    rewrite_links(soup, archive_index, [], "objects/page.html")
    assert soup.find("a")["href"] == "objects__sibling.md#sect"


def test_rewrite_links_relative_html_resolved():
    html = '<a href="#anchor">x</a>'
    soup = parse_html("<html><body>" + html + "</body></html>")
    rewrite_links(soup, {}, [], "p.html")
    assert soup.find("a")["href"] == "#anchor"


def test_rewrite_links_broken_methodicheskaya_dropped():
    soup = parse_html(SAMPLE_METHOD)
    rewrite_links(soup, {}, [], "p")
    text = soup.get_text()
    assert "Методическая информация" in text
    hrefs = [a.get("href") for a in soup.find_all("a")]
    assert all("1centerprise" not in (h or "") for h in hrefs)


def test_to_markdown_escapes_angles_in_link_text():
    from convert import to_markdown
    soup = parse_html(
        '<html><body><a href="x.md">&lt;Имя реквизита&gt; (&lt;Attribute&gt;)</a></body></html>'
    )
    md = to_markdown(soup)
    assert r"[\<Имя реквизита\> (\<Attribute\>)](x.md)" in md


def test_to_markdown_skips_code_blocks():
    from convert import to_markdown
    soup = parse_html(
        "<html><body><pre><code>```\n[no](url) &lt;ok&gt;\n```</code></pre></body></html>"
    )
    md = to_markdown(soup)
    # Backslash-escape NOT applied inside code fences
    assert r"\<" not in md


def test_to_markdown_removes_methodical_info():
    from convert import to_markdown
    soup = parse_html(
        '<html><body><p>Текст</p><p><a href="http://www.1centerprise.com/devlinks?C=\\"x\\">Методическая информация</a></p></body></html>'
    )
    md = to_markdown(soup)
    assert "Методическая информация" not in md
    assert "1centerprise.com/devlinks" not in md


def test_to_markdown_output_has_no_frontmatter_block():
    from convert import to_markdown

    soup = parse_html("<html><body><h1>Заголовок</h1><p>Текст</p></body></html>")
    md = to_markdown(soup)
    assert not md.startswith("---\n")
