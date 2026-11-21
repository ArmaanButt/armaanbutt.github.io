# AGENTS.md

Personal site, deployed to GitHub Pages (armaanbutt.com) by `.github/workflows/deploy.yml`
(Pages source is "GitHub Actions", not branch). No Jekyll. Python 3 plus the `markdown` package.

- Posts are `posts/YYYY-MM-DD-slug.md`; the first line must be `# Title`. `build.py` renders them
  with `post.html` to `/posts/<slug>.html`, lists them in `index.html`, and writes `/feed.xml`.
- Non-Markdown files in `posts/` (images) are copied as-is, so posts can link them relatively.
- Build and preview: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`, then
  `.venv/bin/python build.py && python3 -m http.server -d _site 4000`. There are no tests; a
  successful build is the check.
- Aesthetic is web 1.0: browser-default look, serif text, `#00e` links, no JavaScript.
