#!/usr/bin/env python3
"""Build the site into _site/, filling the post list from the Bear Blog feed.

Usage: python3 build.py && python3 -m http.server -d _site 4000
"""
import datetime
import html
import os
import shutil
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BEAR_BLOG = os.environ.get("BEAR_BLOG", "https://armaanbutt.bearblog.dev")
MAX_POSTS = 20

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
STATIC = ["404.html", "style.css", "favicon.ico", "CNAME"]
ATOM = "{http://www.w3.org/2005/Atom}"


def fetch_posts():
    """Return [(date, title, url)] newest first, or [] if the blog doesn't exist yet."""
    # Bear Blog returns 403 for the default Python User-Agent.
    req = urllib.request.Request(f"{BEAR_BLOG}/feed/", headers={"User-Agent": "Mozilla/5.0 (armaanbutt.com build)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            feed = ET.fromstring(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"warning: {BEAR_BLOG}/feed/ not found, building with no posts")
            return []
        raise  # Fail the build rather than deploy an empty list over a good one.

    posts = []
    for entry in feed.iter(f"{ATOM}entry"):
        published = entry.findtext(f"{ATOM}published") or entry.findtext(f"{ATOM}updated")
        link = entry.find(f"{ATOM}link[@rel='alternate']")
        if link is None:
            link = entry.find(f"{ATOM}link")
        posts.append((published[:10], entry.findtext(f"{ATOM}title", "Untitled"), link.get("href")))
    return sorted(posts, reverse=True)[:MAX_POSTS]


def render_posts(posts):
    if not posts:
        return "<p><i>Nothing here yet.</i></p>"
    items = "\n".join(
        f'<li><span><i><time datetime="{date}">{date}</time></i></span>'
        f'<a href="{html.escape(url)}">{html.escape(title)}</a></li>'
        for date, title, url in posts
    )
    return f'<ul class="blog-posts">\n{items}\n</ul>'


def main():
    posts = fetch_posts()
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    for name in STATIC:
        shutil.copy(ROOT / name, OUT / name)
    page = (ROOT / "index.html").read_text()
    page = page.replace("{{posts}}", render_posts(posts))
    # "Last updated" is the newest post, or today if there are none.
    updated = datetime.date.fromisoformat(posts[0][0]) if posts else datetime.date.today()
    page = page.replace("{{updated}}", updated.strftime("%B %-d, %Y"))
    (OUT / "index.html").write_text(page)
    print(f"built {OUT} with {len(posts)} posts")


if __name__ == "__main__":
    main()
