"""Count incoming cross-references between vault markdown files."""

import io
import re
import sys
from collections import defaultdict
from pathlib import Path

# Force UTF-8 stdout so Cyrillic filenames render correctly on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


LINK_RE = re.compile(r'\[(?:[^\]]*)\]\(([^)#]+\.md)[^)]*\)')


def count_incoming_links(vault_dir: Path, top_n: int = 20) -> None:
    files = list(vault_dir.glob("*.md"))
    file_names = {f.name for f in files}

    incoming: defaultdict[str, int] = defaultdict(int)
    outgoing: defaultdict[str, int] = defaultdict(int)

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = f.read_text(encoding="cp1251", errors="replace")

        targets = LINK_RE.findall(text)
        for target in targets:
            # links may be relative — take just the filename
            target_name = Path(target).name
            if target_name in file_names and target_name != f.name:
                incoming[target_name] += 1
                outgoing[f.name] += 1

    total_files = len(files)
    total_links = sum(incoming.values())
    referenced = len(incoming)
    unreferenced = total_files - referenced

    print(f"Vault: {vault_dir}")
    print(f"Files total   : {total_files}")
    print(f"Links total   : {total_links}")
    print(f"Referenced    : {referenced}")
    print(f"Unreferenced  : {unreferenced}")
    print()

    top = sorted(incoming.items(), key=lambda x: x[1], reverse=True)[:top_n]
    width = max(len(name) for name, _ in top) if top else 40
    width = min(width, 80)

    print(f"Top-{top_n} by incoming links:")
    print(f"{'#':>4}  {'links':>6}  file")
    print("-" * (width + 16))
    for rank, (name, count) in enumerate(top, 1):
        print(f"{rank:>4}  {count:>6}  {name}")


if __name__ == "__main__":
    vault = Path("vault")
    top_n = 20

    args = sys.argv[1:]
    if args:
        try:
            top_n = int(args[0])
        except ValueError:
            vault = Path(args[0])
    if len(args) >= 2:
        try:
            top_n = int(args[1])
        except ValueError:
            pass

    if not vault.is_dir():
        print(f"Error: '{vault}' is not a directory", file=sys.stderr)
        sys.exit(1)

    count_incoming_links(vault, top_n)
