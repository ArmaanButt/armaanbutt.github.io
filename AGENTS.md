# AGENTS.md

Personal homepage, deployed to GitHub Pages (armaanbutt.com) by `.github/workflows/deploy.yml`
(Pages source is "GitHub Actions", not branch). No Jekyll, no dependencies beyond Python 3.

- Blog posts live on Bear Blog (`armaanbutt.bearblog.dev`), not in this repo. `build.py` fetches
  `<blog>/feed/` and writes the post list into `_site/index.html`.
- Bear Blog returns 403 to the default Python/curl User-Agent; keep a `Mozilla/5.0` UA when fetching.
- A 404 feed (blog not created) builds with no posts; any other fetch error fails the build so the
  previous deploy stays live.
- Build and preview: `python3 build.py && python3 -m http.server -d _site 4000`. There are no tests;
  a successful build is the check.
- Aesthetic is web 1.0: browser-default look, serif text, `#00e` links, no JavaScript.
