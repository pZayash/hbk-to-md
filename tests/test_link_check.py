"""Tests for link-integrity check."""

from link_check import (
    check_links,
    remediate_vault_links,
    write_dangling_log,
    write_ungrounded_log,
)


def _md(tmp_path, name: str, body: str) -> None:
    (tmp_path / name).write_text(body, encoding="utf-8")


def test_resolved_and_dangling(tmp_path):
    _md(tmp_path, "A.md", "см. [валюты](Валюты.md) и [сумма](Сумма.md)")
    _md(tmp_path, "Валюты.md", "ничего")
    report = check_links(tmp_path)
    assert report.md_files == 2
    assert report.total_links == 2
    assert report.dangling_targets == 1
    assert "Сумма.md" in report.dangling


def test_links_in_code_fence_ignored(tmp_path):
    _md(
        tmp_path,
        "A.md",
        "текст [реально](Нет.md)\n\n```bsl\n// [в коде](ТожеНет.md)\n```\n",
    )
    report = check_links(tmp_path)
    assert report.total_links == 1
    assert "ТожеНет.md" not in report.dangling
    assert "Нет.md" in report.dangling


def test_meta_files_skipped(tmp_path):
    _md(tmp_path, "_meta.md", "[x](Нет.md)")
    _md(tmp_path, "A.md", "нет ссылок")
    report = check_links(tmp_path)
    assert report.md_files == 1
    assert report.total_links == 0


def test_occurrence_count(tmp_path):
    _md(tmp_path, "A.md", "[a](Нет.md) [b](Нет.md) [c](Нет.md)")
    report = check_links(tmp_path)
    assert report.dangling["Нет.md"][0] == 3
    assert report.dangling_occurrences == 3


def test_dangling_log_written_and_removed(tmp_path):
    _md(tmp_path, "A.md", "[x](Нет.md)")
    report = check_links(tmp_path)
    write_dangling_log(tmp_path, report)
    log = tmp_path / "_dangling.log"
    assert log.exists()
    assert "Нет.md\t1\tA.md" in log.read_text(encoding="utf-8")

    _md(tmp_path, "Нет.md", "теперь есть")
    report2 = check_links(tmp_path)
    write_dangling_log(tmp_path, report2)
    assert not log.exists()


def test_anchor_ungrounded(tmp_path):
    _md(tmp_path, "A.md", "[m](B.md#НетТакого)")
    _md(tmp_path, "B.md", "## Другой\n")
    report = check_links(tmp_path)
    assert report.dangling_targets == 0
    assert report.ungrounded_anchors == 1
    assert "B.md#НетТакого" in report.ungrounded


def test_ungrounded_log_written_and_removed(tmp_path):
    _md(tmp_path, "A.md", "[m](B.md#Нет)")
    _md(tmp_path, "B.md", "## Есть\n")
    report = check_links(tmp_path)
    write_ungrounded_log(tmp_path, report)
    log = tmp_path / "_ungrounded.log"
    assert log.exists()

    _md(tmp_path, "A.md", "[m](B.md#Есть)")
    report2 = check_links(tmp_path)
    write_ungrounded_log(tmp_path, report2)
    assert not log.exists()


def test_remediate_strips_dangling(tmp_path):
    _md(tmp_path, "A.md", "см. [x](Нет.md) и [ok](B.md)")
    _md(tmp_path, "B.md", "есть")
    report = remediate_vault_links(tmp_path)
    assert report.links_stripped == 1
    assert report.files_changed == 1
    text = (tmp_path / "A.md").read_text(encoding="utf-8")
    assert "](Нет.md)" not in text
    assert "x" in text
    assert "[ok](B.md)" in text or "](B.md)" in text


def test_remediate_alias_rewrite(tmp_path):
    _md(tmp_path, "A.md", "[x](old.md)")
    _md(tmp_path, "new.md", "есть")
    report = remediate_vault_links(tmp_path, {"old.md": "new.md"})
    assert report.links_remediated == 1
    assert "[x](new.md)" in (tmp_path / "A.md").read_text(encoding="utf-8")
