# armaanbutt.com

Plain HTML personal site with posts written in Markdown.

## Publishing a post

1. Add `posts/YYYY-MM-DD-slug.md`. The first line is the title:

   ```markdown
   # My first post

   Regular **Markdown** goes here. Tables, footnotes, and fenced code blocks work.
   Images can go in `posts/` too and be linked as `![alt](my-image.jpg)`.
   ```

2. Commit and push to `main`. The Deploy action builds the site and it's live in about a minute.
   You can also do this on github.com: **Add file > Create new file**, name it `posts/2026-11-21-slug.md`, commit.

The post appears at `/posts/slug.html`, on the homepage list, and in `/feed.xml` (RSS/Atom).
To unpublish, delete the file and push.

## Files

- `index.html` is the homepage template. `post.html` is the post template.
- `build.py` renders everything into `_site/`. `.github/workflows/deploy.yml` deploys it to GitHub Pages.

## Run locally

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py && python3 -m http.server -d _site 4000
```
