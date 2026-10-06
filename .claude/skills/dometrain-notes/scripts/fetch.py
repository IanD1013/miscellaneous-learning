"""Fetch the Instructions panel of one or more Dometrain lesson pages as English Markdown.

Usage: fetch.py <lesson-url> [<lesson-url> ...]
Writes one Markdown document per URL to stdout, separated by a "<!-- lesson: URL -->" marker line.
Exits with code 2 if the saved session is not logged in.
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify
from playwright.sync_api import sync_playwright

PROFILE_DIR = Path(__file__).resolve().parent.parent / ".profile"
CONTENT_SELECTOR = "#quiz-instructions-content"


def code_language(el) -> str:
    for cls in el.get("class") or []:
        if cls.startswith("language-"):
            return cls.removeprefix("language-")
    code = el.find("code")
    return code_language(code) if code else ""


def restore_dunders(html: str) -> str:
    """Undo the site's Markdown renderer turning `__init__` into <strong>init</strong> (in headings).

    A <strong> is restored only when its text is a bare identifier whose dunder form appears elsewhere
    in the lesson (usually in code), so genuine bold words are left alone.
    """
    soup = BeautifulSoup(html, "html.parser")
    for strong in soup.find_all("strong"):
        name = strong.get_text()
        if not (re.fullmatch(r"[a-z][a-z0-9_]*", name) and f"__{name}__" in html):
            continue
        # Pull a dotted prefix such as "super()." into the same code span.
        prefix = ""
        prev = strong.previous_sibling
        if isinstance(prev, NavigableString) and (m := re.search(r"[\w().]*\.$", prev)):
            prefix = m.group()
            prev.replace_with(prev[: m.start()])
        code = soup.new_tag("code")
        code.string = f"{prefix}__{name}__"
        strong.replace_with(code)
    return str(soup)


def to_markdown(html: str) -> str:
    md = markdownify(restore_dunders(html), heading_style="ATX", bullets="-", code_language_callback=code_language)
    return re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"


def main(urls: list[str]) -> None:
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, channel="chrome", headless=True)
        page = ctx.new_page()
        for url in urls:
            page.goto(url, wait_until="networkidle")
            content = page.locator(CONTENT_SELECTOR)
            if content.count() == 0:
                logged_out = page.get_by_text("Enroll to continue").count() > 0
                ctx.close()
                if logged_out:
                    print("Not logged in: re-export cookies.txt and run import_cookies.py.", file=sys.stderr)
                    sys.exit(2)
                sys.exit(f"No {CONTENT_SELECTOR} found on {url}")
            print(f"<!-- lesson: {url} -->")
            print(to_markdown(content.inner_html()))
        ctx.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
