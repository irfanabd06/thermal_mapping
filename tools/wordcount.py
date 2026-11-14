"""Count words in the report for the CDE4301 3,000-word limit.

Reads the section files listed in REPORT_SECTIONS in docs/report-loader.js
(so references and appendices are excluded), and skips:
  - "> TODO" draft notes,
  - [[table: ...]] shortcodes (table contents live in report-tables.js),
  - image lines, HTML comments and Markdown syntax characters.

Usage: python3 tools/wordcount.py
"""

import re
import sys
from pathlib import Path

LIMIT = 3000
DOCS = Path(__file__).resolve().parent.parent / "docs"


def report_sections():
    loader = (DOCS / "report-loader.js").read_text(encoding="utf-8")
    block = re.search(r"const REPORT_SECTIONS = \[(.*?)\];", loader, re.S).group(1)
    return re.findall(r'"([^"]+\.md)"', block)


def count_words(markdown):
    title = ""
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n?", markdown, re.S)
    if fm:
        t = re.search(r"^title:\s*(.*)$", fm.group(1), re.M)
        title = t.group(1).strip("\"'") if t else ""
        markdown = markdown[fm.end():]

    markdown = re.sub(r"<!--.*?-->", " ", markdown, flags=re.S)
    kept, in_todo = [], False
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            if re.match(r">\s*TODO\b", stripped, re.I):
                in_todo = True
            if in_todo:
                continue
        else:
            in_todo = False
        if re.match(r"^\\?\[\\?\[\s*table\s*:", stripped, re.I) or re.match(r"^!\[.*\]\(.*\)$", stripped):
            continue
        kept.append(line)

    text = title + "\n" + "\n".join(kept)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)   # links -> link text
    text = re.sub(r"[#>*_`|]", " ", text)                    # markdown syntax
    text = re.sub(r"^\s*(\d+\.|-)\s+", " ", text, flags=re.M)  # list markers
    return len(re.findall(r"\S+", text))


def main():
    total = 0
    print("Word count (report body only; TODO notes, tables, references and appendices excluded)\n")
    for name in report_sections():
        n = count_words((DOCS / "sections" / name).read_text(encoding="utf-8"))
        total += n
        print(f"  {n:5d}  {name}")
    print(f"  {'-' * 5}")
    print(f"  {total:5d}  total  ({LIMIT - total:+d} vs {LIMIT}-word limit)")
    if total > LIMIT:
        sys.exit(1)


if __name__ == "__main__":
    main()
