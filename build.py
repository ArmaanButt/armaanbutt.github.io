#!/usr/bin/env python3
"""Build the site into _site/ from the Markdown posts in posts/.

A post is posts/YYYY-MM-DD-slug.md whose first line is "# Title".
It is published at /posts/slug.html.

Usage: pip install -r requirements.txt
       python3 build.py && python3 -m http.server -d _site 4000
"""
import datetime
import html
import re
import shutil
from pathlib import Path

import markdown

SITE = "https://armaanbutt.com"
AUTHOR = "Armaan Butt"

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
STATIC = ["404.html", "style.css", "favicon.ico", "CNAME"]
POST_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)\.md")


def load_posts():
    """Return posts newest first, as dicts with date, slug, title, url, and body HTML."""
    posts = []
    for path in (ROOT / "posts").glob("*.md"):
        match = POST_NAME.fullmatch(path.name)
        if not match:
            raise SystemExit(f"{path}: name must look like YYYY-MM-DD-slug.md")
        date, slug = match.groups()
        first, _, rest = path.read_text().partition("\n")
        if not first.startswith("# "):
            raise SystemExit(f"{path}: first line must be '# Title'")
        posts.append({
            "date": datetime.date.fromisoformat(date),
            "slug": slug,
            "title": first[2:].strip(),
            "url": f"/posts/{slug}.html",
            "body": markdown.markdown(rest, extensions=["extra", "sane_lists"]),
        })
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def fill(template, **values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def render_list(posts):
    if not posts:
        return "<p><i>Nothing here yet.</i></p>"
    items = "\n".join(
        f'<li><span><time datetime="{p["date"]}">{p["date"]}</time></span>'
        f'<a href="{p["url"]}">{html.escape(p["title"])}</a></li>'
        for p in posts
    )
    return f'<ul class="posts">\n{items}\n</ul>'


def render_feed(posts, updated):
    entries = "".join(
        f"""
<entry>
<title>{html.escape(p["title"])}</title>
<link href="{SITE}{p["url"]}"/>
<id>{SITE}{p["url"]}</id>
<updated>{p["date"]}T00:00:00Z</updated>
<content type="html">{html.escape(p["body"])}</content>
</entry>"""
        for p in posts
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>{AUTHOR}</title>
<link href="{SITE}/"/>
<link rel="self" href="{SITE}/feed.xml"/>
<id>{SITE}/</id>
<author><name>{AUTHOR}</name></author>
<updated>{updated}T00:00:00Z</updated>{entries}
</feed>
"""


def main():
    posts = load_posts()
    # "Last updated" is the newest post, or today if there are none.
    updated = posts[0]["date"] if posts else datetime.date.today()

    shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "posts").mkdir(parents=True)
    for name in STATIC:
        shutil.copy(ROOT / name, OUT / name)
    # Images and other files next to posts, so posts can link them relatively.
    for path in (ROOT / "posts").glob("*"):
        if path.is_file() and path.suffix != ".md":
            shutil.copy(path, OUT / "posts" / path.name)

    post_template = (ROOT / "post.html").read_text()
    for p in posts:
        page = fill(post_template, title=html.escape(p["title"]), date=str(p["date"]), content=p["body"])
        (OUT / p["url"].lstrip("/")).write_text(page)

    index = fill((ROOT / "index.html").read_text(),
                 posts=render_list(posts), updated=updated.strftime("%B %-d, %Y"))
    (OUT / "index.html").write_text(index)
    (OUT / "feed.xml").write_text(render_feed(posts, updated))
    print(f"built {OUT} with {len(posts)} posts")


if __name__ == "__main__":
    main()
