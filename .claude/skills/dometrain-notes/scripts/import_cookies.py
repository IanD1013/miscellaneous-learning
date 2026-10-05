"""Import a Netscape-format cookies.txt (e.g. from the "Get cookies.txt LOCALLY" extension) into the Dometrain profile.

Usage: import_cookies.py <cookies.txt>
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE_DIR = Path(__file__).resolve().parent.parent / ".profile"


def parse(path: Path) -> list[dict]:
    cookies = []
    for line in path.read_text().splitlines():
        http_only = line.startswith("#HttpOnly_")
        if http_only:
            line = line.removeprefix("#HttpOnly_")
        if not line.strip() or line.startswith("#"):
            continue
        domain, _, cookie_path, secure, expires, name, value = line.split("\t")
        if "dometrain.com" not in domain:
            continue
        cookie = {"name": name, "value": value, "domain": domain, "path": cookie_path,
                  "secure": secure == "TRUE", "httpOnly": http_only}
        if int(expires) > 0:
            cookie["expires"] = int(expires)
        cookies.append(cookie)
    return cookies


cookies = parse(Path(sys.argv[1]))
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(PROFILE_DIR, channel="chrome", headless=True)
    ctx.add_cookies(cookies)
    ctx.close()
print(f"Imported {len(cookies)} dometrain.com cookies.")
