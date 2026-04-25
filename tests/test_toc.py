"""Тесты генерации TOC (_index*.md)."""

from pathlib import Path

from convert import (
    ALPHA_GROUP_THRESHOLD,
    TreeNode,
    build_hierarchy,
    compute_page_counts,
    infer_title_from_children,
    index_filename_for,
    propagate_titles,
    render_index,
    render_inline_toc,
    render_root_index,
    simplify_table_section_title,
    write_all_indexes,
)


def _sample_pages_meta() -> dict[str, dict]:
    return {
        "objects__Global_context.md": {
            "source_path": "objects/Global context.html",
            "title_ru": "Глобальный контекст",
            "title_en": "",
        },
        "objects__Global_context__methods__A1.md": {
            "source_path": "objects/Global context/methods/A1.html",
            "title_ru": "Альфа",
            "title_en": "",
        },
        "objects__Global_context__methods__B1.md": {
            "source_path": "objects/Global context/methods/B1.html",
            "title_ru": "Бета",
            "title_en": "",
        },
    }


def _find_node(root: TreeNode, prefix: str) -> TreeNode:
    if root.prefix == prefix:
        return root
    for child in root.children.values():
        found = _find_node(child, prefix)
        if found:
            return found
    raise AssertionError(f"node {prefix} not found")


def test_build_hierarchy_simple():
    pages_meta = _sample_pages_meta()
    tree = build_hierarchy({}, pages_meta)
    methods = _find_node(tree, "objects/Global context/methods")
    assert methods.segment == "methods"
    assert "A1" in methods.children
    assert methods.children["A1"].content_filename == "objects__Global_context__methods__A1.md"


def test_propagate_titles_known_segment():
    pages_meta = _sample_pages_meta()
    tree = build_hierarchy({}, pages_meta)
    propagate_titles(tree, pages_meta)
    methods = _find_node(tree, "objects/Global context/methods")
    assert methods.title == "Методы"


def test_propagate_titles_from_content_page():
    pages_meta = _sample_pages_meta()
    tree = build_hierarchy({}, pages_meta)
    propagate_titles(tree, pages_meta)
    node = _find_node(tree, "objects/Global context")
    assert node.title == "Глобальный контекст"


def test_index_filename_for():
    assert index_filename_for("objects/Global context/methods") == "_index__objects__Global_context__methods.md"


def test_render_index_subsections_only():
    node = TreeNode(prefix="objects", segment="objects", title="Объекты")
    child = TreeNode(prefix="objects/Global context", segment="Global context", title="Глобальный контекст", page_count=5)
    child.children["x"] = TreeNode(prefix="objects/Global context/x", segment="x", title="x")
    node.children["Global context"] = child
    content = render_index(node, "_index.md", {}, {"_index.md"}, {"objects": node, "objects/Global context": child})
    assert "## Подразделы (1)" in content
    assert "## Страницы" not in content


def test_render_index_pages_only():
    node = TreeNode(prefix="objects/Global context/methods", segment="methods", title="Методы")
    node.children["A"] = TreeNode(
        prefix="objects/Global context/methods/A",
        segment="A",
        title="Альфа",
        content_filename="a.md",
    )
    content = render_index(node, "_index__objects__Global_context.md", {}, {"_index.md"}, {"objects/Global context/methods": node})
    assert "## Страницы (1)" in content
    assert "## Подразделы" not in content


def test_render_index_alpha_grouping():
    node = TreeNode(prefix="objects/Global context/methods", segment="methods", title="Методы")
    for i in range(ALPHA_GROUP_THRESHOLD + 1):
        title = f"А{i:02d}"
        node.children[f"m{i}"] = TreeNode(
            prefix=f"objects/Global context/methods/m{i}",
            segment=f"m{i}",
            title=title,
            content_filename=f"m{i}.md",
        )
    content = render_index(node, "_index__objects__Global_context.md", {}, {"_index.md"}, {"objects/Global context/methods": node})
    assert "### А" in content


def test_root_index_no_breadcrumb():
    root = TreeNode(prefix="", segment="")
    root.children["objects"] = TreeNode(prefix="objects", segment="objects", title="Объекты", page_count=10)
    content = render_root_index(root, "8.3.27.1786", 10)
    assert "**↑** [Главная]" not in content
    assert "_index__objects.md" in content


def test_compute_page_counts():
    pages_meta = _sample_pages_meta()
    tree = build_hierarchy({}, pages_meta)
    propagate_titles(tree, pages_meta)
    total = compute_page_counts(tree)
    assert total == 3


def test_infer_tables_catalog_title_from_children():
    node = TreeNode(prefix="tables/catalog1", segment="catalog1")
    node.children["table2"] = TreeNode(
        prefix="tables/catalog1/table2",
        segment="table2",
        title="РегистрСведений.<Имя регистра сведений>",
        content_filename="tables__catalog1__table2.md",
    )
    node.children["table3"] = TreeNode(
        prefix="tables/catalog1/table3",
        segment="table3",
        title="РегистрСведений.<Имя регистра сведений>.СрезПоследних",
        content_filename="tables__catalog1__table3.md",
    )
    assert infer_title_from_children(node) == "РегистрСведений"


def test_simplify_table_section_title():
    assert simplify_table_section_title("Документ.<Имя документа>") == "Документ"
    assert (
        simplify_table_section_title("БизнесПроцесс.<Имя бизнес-процесса>.Точки")
        == "БизнесПроцесс.Точки"
    )


def test_render_index_simplifies_tables_subsections():
    node = TreeNode(prefix="tables/catalog63", segment="catalog63", title="ТаблицыИзменений")
    node.children["table69"] = TreeNode(
        prefix="tables/catalog63/table69",
        segment="table69",
        title="БизнесПроцесс.<Имя бизнес-процесса>.Изменения",
    )
    node.children["table66"] = TreeNode(
        prefix="tables/catalog63/table66",
        segment="table66",
        title="Документ.<Имя документа>.Изменения",
    )
    # делаем их подразделами (есть потомки)
    node.children["table69"].children["f"] = TreeNode(prefix="x", segment="x")
    node.children["table66"].children["f"] = TreeNode(prefix="y", segment="y")
    content = render_index(
        node,
        "_index__tables.md",
        {},
        {"_index.md"},
        {"tables/catalog63": node},
    )
    assert "БизнесПроцесс.Изменения" in content
    assert "Документ.Изменения" in content


def test_infer_tables_catalog_changes_title():
    node = TreeNode(prefix="tables/catalog63", segment="catalog63")
    node.children["table69"] = TreeNode(
        prefix="tables/catalog63/table69",
        segment="table69",
        title="БизнесПроцесс.<Имя бизнес-процесса>.Изменения",
        content_filename="tables__catalog63__table69.md",
    )
    node.children["table66"] = TreeNode(
        prefix="tables/catalog63/table66",
        segment="table66",
        title="Документ.<Имя документа>.Изменения",
        content_filename="tables__catalog63__table66.md",
    )
    node.children["table64"] = TreeNode(
        prefix="tables/catalog63/table64",
        segment="table64",
        title="Константа.<Имя константы>.Изменения",
        content_filename="tables__catalog63__table64.md",
    )
    assert infer_title_from_children(node) == "ТаблицыИзменений"


def test_write_all_indexes_skips_node_with_content(tmp_path: Path):
    root = TreeNode(prefix="", segment="")
    section = TreeNode(prefix="objects/catalog2", segment="catalog2", title="Системные перечисления", content_filename="objects__catalog2.md")
    child = TreeNode(prefix="objects/catalog2/x", segment="x", title="X", content_filename="objects__catalog2__x.md")
    section.children["x"] = child
    root.children["objects"] = TreeNode(prefix="objects", segment="objects", title="Объекты")
    root.children["objects"].children["catalog2"] = section
    count, files = write_all_indexes(root, Path(tmp_path), {})
    assert "_index__objects__catalog2.md" not in files
    assert count == 1


def test_render_inline_toc():
    node = TreeNode(prefix="objects/catalog2", segment="catalog2", title="Системные перечисления")
    subsection = TreeNode(prefix="objects/catalog2/sub", segment="sub", title="Подраздел", page_count=3, content_filename="objects__catalog2__sub.md")
    subsection.children["leaf"] = TreeNode(prefix="objects/catalog2/sub/leaf", segment="leaf", title="leaf")
    page = TreeNode(prefix="objects/catalog2/p", segment="p", title="Страница", content_filename="objects__catalog2__p.md")
    node.children["sub"] = subsection
    node.children["p"] = page
    toc = render_inline_toc(node)
    assert "## Оглавление" in toc
    assert "objects__catalog2__sub.md" in toc
