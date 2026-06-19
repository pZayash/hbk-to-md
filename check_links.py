"""CLI: проверка целостности ссылок в готовом vault."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from link_check import (
    check_links,
    remediate_vault_links,
    write_dangling_log,
    write_ungrounded_log,
)


def verify_links(out_dir: Path, fix: bool = False) -> int:
    if not out_dir.is_dir():
        print(f"Каталог не найден: {out_dir}", file=sys.stderr)
        return 1

    if fix:
        report_fix = remediate_vault_links(out_dir)
        print(
            f"Исправление: файлов={report_fix.files_changed} "
            f"алиасов={report_fix.links_remediated} "
            f"убрано_висячих={report_fix.links_stripped}",
            file=sys.stderr,
        )

    report = check_links(out_dir)
    write_dangling_log(out_dir, report)
    write_ungrounded_log(out_dir, report)

    print(
        f"Проверка ссылок: файлов={report.md_files} ссылок={report.total_links} "
        f"целей={report.unique_targets} висячих={report.dangling_targets} "
        f"(вхождений={report.dangling_occurrences})",
        file=sys.stderr,
    )
    if report.by_prefix:
        top = sorted(report.by_prefix.items(), key=lambda kv: -kv[1])
        breakdown = ", ".join(f"{p}={c}" for p, c in top[:12])
        print(f"Висячие по префиксам: {breakdown}", file=sys.stderr)
    if report.dangling:
        print(f"Подробности: {out_dir / '_dangling.log'}", file=sys.stderr)
    if report.anchor_links:
        print(
            f"Заземление якорей: с якорем={report.anchor_links} "
            f"незаземлённых={report.ungrounded_anchors} "
            f"(вхождений={report.ungrounded_occurrences})",
            file=sys.stderr,
        )
        if report.ungrounded:
            print(f"Подробности: {out_dir / '_ungrounded.log'}", file=sys.stderr)
    return 0 if report.dangling_targets == 0 else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Проверка висячих ссылок в готовом каталоге .md (без конвертации)",
    )
    parser.add_argument(
        "vault",
        nargs="?",
        type=Path,
        default=Path("vault"),
        help="Каталог vault (по умолчанию: vault)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Убрать висячие ссылки (plain text) перед проверкой",
    )
    args = parser.parse_args(argv)
    return verify_links(args.vault.resolve(), fix=args.fix)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
