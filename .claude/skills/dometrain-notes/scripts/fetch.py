"""Fetch the Instructions panel of one or more Dometrain lesson pages as Markdown.

Usage: fetch.py <lesson-url> [<lesson-url> ...]
Writes one Markdown document per URL to stdout, each after a "<!-- lesson: URL lang: en|zh -->" marker line.
Hands-on exercise lessons offer a site translation; it is selected so their content comes back in Simplified
Chinese (lang: zh), followed by a "<!-- task -->" ... "<!-- /task -->" block holding the editor code and test
cases. Quiz lessons have no translation or task block and come back in English (lang: en).
Exits with code 2 if the saved session is not logged in.
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify
from playwright.sync_api import sync_playwright

PROFILE_DIR = Path(__file__).resolve().parent.parent / ".profile"
QUIZ_SELECTOR = "#quiz-instructions-content"
EXERCISE_SELECTOR = "#exercise-instructions"
TRANSLATION_DROPDOWN = "#translation-dropdown"
TRANSLATION_LANG = "zh"


def code_language(el) -> str:
    for cls in el.get("class") or []:
        if cls.startswith("language-"):
            lang = cls.removeprefix("language-")
            # The exercise renderer emits "language-undefined" for unlabeled blocks.
            return "" if lang == "undefined" else lang
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


def strip_hints(html: str) -> str:
    """Drop the exercise's collapsible Hints section, which is not part of the lesson text."""
    soup = BeautifulSoup(html, "html.parser")
    for hints in soup.select(".hints-section"):
        hints.decompose()
    return str(soup)


def select_translation(page) -> None:
    """Switch the exercise instructions to the site's Simplified Chinese translation and wait for it to render."""
    item = page.locator(f'.translation-menu-item[data-lang="{TRANSLATION_LANG}"]')
    if "selected" in (item.get_attribute("class") or "").split():
        return
    before = page.locator(EXERCISE_SELECTOR).inner_text()
    # JS clicks: the first-visit tour overlay intercepts pointer events.
    page.locator(TRANSLATION_DROPDOWN).evaluate("el => el.click()")
    item.evaluate("el => el.click()")
    page.wait_for_function(
        """([sel, before]) => {
            const loading = document.getElementById("translation-loading");
            const busy = loading && getComputedStyle(loading).display !== "none";
            return !busy && document.querySelector(sel).innerText !== before;
        }""",
        arg=[EXERCISE_SELECTOR, before],
    )


def lesson_html(page) -> tuple[str, str] | None:
    """Return (lang, inner HTML) of the lesson's instructions, or None if neither layout is on the page."""
    if page.locator(EXERCISE_SELECTOR).count():
        if page.locator(TRANSLATION_DROPDOWN).is_visible():
            select_translation(page)
            lang = TRANSLATION_LANG
        else:
            lang = "en"
        return lang, strip_hints(page.locator(EXERCISE_SELECTOR).inner_html())
    if page.locator(QUIZ_SELECTOR).count():
        return "en", page.locator(QUIZ_SELECTOR).inner_html()
    return None


def exercise_task(page) -> str:
    """Return the exercise's editor code and test cases as a marked block, or "" for a quiz lesson.

    This is input for solving the lesson's "Your Task", not lesson text to translate.
    """
    if not page.locator(EXERCISE_SELECTOR).count():
        return ""
    page.wait_for_function("() => window.monaco && monaco.editor.getEditors()[0]?.getModel()")
    parts = ["<!-- task: editor code and test cases, for solving only -->"]
    # One tab per file; read-only tabs are support files the solution uses but must not change.
    for tab in page.locator(".editor-tab").all():
        tab.evaluate("el => el.click()")
        language, code = page.evaluate(
            "() => { const m = monaco.editor.getEditors()[0].getModel(); return [m.getLanguageId(), m.getValue()]; }"
        )
        readonly = " (read-only)" if "readonly" in (tab.get_attribute("class") or "").split() else ""
        parts.append(f"File: {tab.get_attribute('data-file-name')}{readonly}\n\n```{language}\n{code.rstrip()}\n```")
    for i, case in enumerate(page.locator("#test-cases-list .test-case-item").all(), 1):
        parts.append(f"Test {i}: {case.locator('.test-case-item-name').inner_text()}")
        for group in case.locator(".test-case-io-group").all():
            label = group.locator(".test-case-io-label").inner_text()
            value = group.locator(".test-case-io-value").inner_text()
            parts.append(f"{label}:\n```\n{value}\n```")
    parts.append("<!-- /task -->")
    return "\n\n".join(parts) + "\n"


def to_markdown(html: str) -> str:
    md = markdownify(restore_dunders(html), heading_style="ATX", bullets="-", code_language_callback=code_language)
    return re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"


def main(urls: list[str]) -> None:
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, channel="chrome", headless=True)
        page = ctx.new_page()
        for url in urls:
            page.goto(url, wait_until="networkidle")
            lesson = lesson_html(page)
            if lesson is None:
                logged_out = page.get_by_text("Enroll to continue").count() > 0
                ctx.close()
                if logged_out:
                    print("Not logged in: re-export cookies.txt and run import_cookies.py.", file=sys.stderr)
                    sys.exit(2)
                sys.exit(f"Neither {EXERCISE_SELECTOR} nor {QUIZ_SELECTOR} found on {url}")
            lang, html = lesson
            print(f"<!-- lesson: {url} lang: {lang} -->")
            print(to_markdown(html))
            if task := exercise_task(page):
                print(task)
        ctx.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
