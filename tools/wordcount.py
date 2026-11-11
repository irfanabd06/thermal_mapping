"""Count words in the report body for the CDE4301 3,000-word limit.

Counts text inside <div id="report-body"> in docs/index.html, skipping
draft placeholders (class="todo"), HTML comments and scripts.
References and appendices sit outside #report-body, so they are not counted.

Usage: python3 tools/wordcount.py [path/to/index.html]
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

LIMIT = 3000
VOID_TAGS = {"br", "img", "hr", "meta", "link", "input", "source", "area", "base", "col", "embed", "wbr"}


class BodyCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0          # nesting depth inside #report-body (0 = outside)
        self.skip_depth = 0     # nesting depth inside a skipped element
        self.section = "(before first heading)"
        self.in_heading = False
        self.heading_text = ""
        self.counts = {}

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        attrs = dict(attrs)
        if self.depth == 0:
            if attrs.get("id") == "report-body":
                self.depth = 1
            return
        self.depth += 1
        if self.skip_depth:
            self.skip_depth += 1
        elif "todo" in (attrs.get("class") or "").split() or tag in ("script", "style"):
            self.skip_depth = 1
        if tag == "h2" and not self.skip_depth:
            self.in_heading = True
            self.heading_text = ""

    def handle_endtag(self, tag):
        if tag in VOID_TAGS or self.depth == 0:
            return
        if tag == "h2" and self.in_heading:
            self.in_heading = False
            self.section = self.heading_text.strip()
        if self.skip_depth:
            self.skip_depth -= 1
        self.depth -= 1

    def handle_data(self, data):
        if self.depth == 0 or self.skip_depth:
            return
        if self.in_heading:
            self.heading_text += data
        words = len(re.findall(r"\S+", data))
        if words:
            self.counts[self.section] = self.counts.get(self.section, 0) + words


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "docs" / "index.html"
    parser = BodyCounter()
    parser.feed(path.read_text(encoding="utf-8"))

    total = sum(parser.counts.values())
    print(f"Word count for {path} (tables rendered by JavaScript are not included)\n")
    for section, n in parser.counts.items():
        print(f"  {n:5d}  {section}")
    print(f"  {'-' * 5}")
    print(f"  {total:5d}  total  ({LIMIT - total:+d} vs {LIMIT}-word limit)")
    if total > LIMIT:
        sys.exit(1)


if __name__ == "__main__":
    main()
