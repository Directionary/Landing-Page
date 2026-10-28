"""Landing-page static checks (no dependencies).

Run: python3 scripts/validate.py [repo-root]
Checks:
  - required files exist (pages, styles, theme.js, favicons, CNAME)
  - CNAME is a bare hostname (no scheme, no path)
  - every page has lang, viewport, title, theme-color meta, theme.js
  - every internal href/src resolves to a file in the repo
  - every #fragment link resolves to an id in its target page
External http(s)/mailto:/tel:/data: links are skipped (lychee territory).
Exit 1 on any error; warnings go to stdout but do not fail.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent

PAGES = [
    "index.html",
    "about/index.html",
    "features/index.html",
    "privacy/index.html",
    "support/index.html",
    "terms/index.html",
]
REQUIRED = PAGES + [
    "styles.css",
    "assets/theme.js",
    "assets/favicon.png",
    "assets/apple-touch-icon.png",
    "CNAME",
]

VOID = re.compile(r"^(#|mailto:|tel:|data:)", re.I)


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []  # (attr, value, line)
        self.ids = set()
        self.metas = []
        self.html_lang = None
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        pos = self.getpos()[0]
        if tag == "html":
            self.html_lang = d.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and "name" in d:
            self.metas.append((d.get("name"), d.get("content"), d.get("media")))
        if tag == "a" and d.get("href"):
            self.refs.append(("href", d["href"], pos))
        if tag == "link" and d.get("href"):
            self.refs.append(("href", d["href"], pos))
        if tag in ("img", "script", "source") and d.get("src"):
            self.refs.append(("src", d["src"], pos))
        if d.get("id"):
            self.ids.add(d["id"])

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def parse(page: Path) -> Collector:
    c = Collector()
    c.feed(page.read_text(encoding="utf-8"))
    return c


def resolve_target(ref: str, page_rel: str):
    """Return (repo-relative path or None if external/void, fragment or '')."""
    if not ref or VOID.match(ref) or ref.startswith(("http://", "https://", "//")):
        return None, ""
    nomedia = ref.split("?", 1)[0]
    path_part, _, frag = nomedia.partition("#")
    if not path_part:  # pure #fragment on same page
        return page_rel, frag
    if path_part.startswith("/"):  # root-relative: / -> index.html
        rel = path_part.lstrip("/")
        if rel == "":
            return "index.html", frag
        p = ROOT / rel
        if p.is_dir():
            return f"{rel.rstrip('/')}/index.html", frag
        return rel, frag
    # relative to the page's directory
    base = (ROOT / page_rel).parent
    target = (base / path_part).resolve()
    try:
        return str(target.relative_to(ROOT.resolve())), frag
    except ValueError:
        return None, ""


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    cname = ROOT / "CNAME"
    if cname.is_file():
        body = cname.read_text(encoding="utf-8").strip()
        if not body or "/" in body or body.startswith(("http", " ")):
            errors.append(f"CNAME must be a bare hostname, got: {body!r}")

    id_cache: dict[str, set[str]] = {}

    def ids_of(rel: str) -> set[str]:
        if rel not in id_cache:
            p = ROOT / rel
            id_cache[rel] = parse(p).ids if p.is_file() else set()
        return id_cache[rel]

    for page_rel in PAGES:
        page = ROOT / page_rel
        if not page.is_file():
            continue
        try:
            col = parse(page)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{page_rel}: unparsable HTML: {e}")
            continue
        if col.html_lang != "en":
            errors.append(f"{page_rel}: <html lang> must be 'en'")
        if not (col.title or "").strip():
            errors.append(f"{page_rel}: missing <title>")
        raw = page.read_text(encoding="utf-8")
        if 'name="viewport"' not in raw:
            errors.append(f"{page_rel}: missing viewport meta")
        if 'name="theme-color"' not in raw:
            errors.append(f"{page_rel}: missing theme-color meta")
        if "theme.js" not in raw:
            errors.append(f"{page_rel}: missing theme.js script tag")
        for attr, ref, line in col.refs:
            target_rel, frag = resolve_target(ref, page_rel)
            if target_rel is None:
                continue
            if not (ROOT / target_rel).is_file():
                errors.append(f"{page_rel}:{line}: broken {attr}={ref!r} -> {target_rel!r} missing")
                continue
            if frag and frag not in ids_of(target_rel):
                # tolerate top-level route anchors handled client-side? none here.
                errors.append(
                    f"{page_rel}:{line}: {attr}={ref!r} fragment #{frag} not found in {target_rel}"
                )

    for e in errors:
        print(f"ERROR {e}")
    for w in warnings:
        print(f"WARN {w}")
    print(f"checked {len(PAGES)} pages, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
