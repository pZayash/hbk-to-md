"""Тесты breadcrumb-генератора."""

from pathlib import Path

from convert import (
    TreeNode,
    inject_breadcrumb_into_content,
    render_breadcrumb,
    resolve_breadcrumb_target,
    walk_parents,
)


def test_walk_parents_deep():
    out = walk_parents("objects/Global context/methods/catalog1566/CanReadXML1628")
    assert out == [
        "objects",
        "objects/Global context",
        "objects/Global context/methods",
        "objects/Global context/methods/catalog1566",
    ]


def test_resolve_target_content_priority():
    archive_index = {
        "objects/global context.html": "objects__Global_context.md",
    }
    index_files = {"_index__objects__Global_context.md"}
    node = TreeNode(prefix="objects/Global context", segment="Global context", title="Глобальный контекст")
    resolved = resolve_breadcrumb_target(
        "objects/Global context",
        archive_index,
        index_files,
        {"objects/Global context": node},
    )
    assert resolved == ("objects__Global_context.md", "Глобальный контекст")


def test_resolve_target_index_fallback():
    archive_index: dict[str, str] = {}
    index_files = {"_index__objects__Global_context__methods.md"}
    node = TreeNode(prefix="objects/Global context/methods", segment="methods", title="Методы")
    resolved = resolve_breadcrumb_target(
        "objects/Global context/methods",
        archive_index,
        index_files,
        {"objects/Global context/methods": node},
    )
    assert resolved == ("_index__objects__Global_context__methods.md", "Методы")


def test_resolve_target_skip():
    resolved = resolve_breadcrumb_target("objects/unknown", {}, set(), {})
    assert resolved is None


def test_render_breadcrumb_format():
    archive_index = {
        "objects/global context.html": "objects__Global_context.md",
        "objects/global context/methods/catalog1566.html": "objects__Global_context__methods__catalog1566.md",
    }
    index_files = {
        "_index.md",
        "_index__objects.md",
        "_index__objects__Global_context__methods.md",
    }
    prefix_map = {
        "objects": TreeNode(prefix="objects", segment="objects", title="Объекты"),
        "objects/Global context": TreeNode(prefix="objects/Global context", segment="Global context", title="Глобальный контекст"),
        "objects/Global context/methods": TreeNode(prefix="objects/Global context/methods", segment="methods", title="Методы"),
        "objects/Global context/methods/catalog1566": TreeNode(
            prefix="objects/Global context/methods/catalog1566",
            segment="catalog1566",
            title="Группа методов",
        ),
    }
    line = render_breadcrumb(
        "objects/Global context/methods/catalog1566/CanReadXML1628",
        archive_index,
        index_files,
        prefix_map,
    )
    assert line.startswith("**↑** [Главная](_index.md)")
    assert " › [Объекты](_index__objects.md)" in line
    assert " › [Глобальный контекст](objects__Global_context.md)" in line


def test_render_breadcrumb_root_only():
    line = render_breadcrumb(
        "objects/Global context",
        {},
        {"_index.md", "_index__objects.md"},
        {"objects": TreeNode(prefix="objects", segment="objects", title="Объекты")},
    )
    assert line == "**↑** [Главная](_index.md) › [Объекты](_index__objects.md)"


def test_inject_breadcrumb_after_frontmatter(tmp_path: Path):
    file = tmp_path / "page.md"
    file.write_text("---\ntitle_ru: \"X\"\n---\n# Заголовок\n", encoding="utf-8")
    ok = inject_breadcrumb_into_content(file, "**↑** [Главная](_index.md)")
    assert ok is True
    text = file.read_text(encoding="utf-8")
    assert text.splitlines()[3] == "**↑** [Главная](_index.md)"


def test_inject_breadcrumb_no_frontmatter(tmp_path: Path):
    file = tmp_path / "page.md"
    file.write_text("# Заголовок\n", encoding="utf-8")
    ok = inject_breadcrumb_into_content(file, "**↑** [Главная](_index.md)")
    assert ok is True
    text = file.read_text(encoding="utf-8")
    assert text.startswith("**↑** [Главная](_index.md)\n\n# Заголовок")
