"""List the lessons of one module (chapter) of a Dometrain course, in course order.

Usage: list_lessons.py <course-or-lesson-url> "<module name>"
Prints one "URL<TAB>lesson title" line per lesson. The module name matches the sidebar's chapter title, ignoring case.
Exits with code 2 if the saved session is not logged in.
"""
import sys
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from fetch import PROFILE_DIR

CHAPTER_SELECTOR = "#curriculum-sidebar .curriculum-chapter"


def main(url: str, module: str) -> None:
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, channel="chrome", headless=True)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        chapters = page.locator(CHAPTER_SELECTOR).all()
        if not chapters:
            logged_out = page.get_by_text("Enroll to continue").count() > 0
            ctx.close()
            if logged_out:
                print("Not logged in: re-export cookies.txt and run import_cookies.py.", file=sys.stderr)
                sys.exit(2)
            sys.exit(f"No course sidebar ({CHAPTER_SELECTOR}) found on {url}")
        titles = [c.locator(".chapter-title").inner_text().strip() for c in chapters]
        matches = [c for c, t in zip(chapters, titles) if t.casefold() == module.strip().casefold()]
        if not matches:
            ctx.close()
            sys.exit(f"No module named {module!r}. Modules:\n" + "\n".join(titles))
        for link in matches[0].locator("a.lesson-item").all():
            title = link.get_attribute("title") or link.inner_text().strip()
            print(f"{urljoin(page.url, link.get_attribute('href'))}\t{title}")
        ctx.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
