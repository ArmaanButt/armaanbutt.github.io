# armaanbutt.com

Plain HTML homepage. Posts are written on [Bear Blog](https://armaanbutt.bearblog.dev) and the
homepage lists them by reading its Atom feed at build time.

- `index.html` is the homepage template (`{{posts}}` and `{{updated}}` are filled in by `build.py`).
- `style.css` is shared with the Bear Blog. Paste it into Bear's theme editor so the two match.
- `.github/workflows/deploy.yml` builds and deploys to GitHub Pages on every push and hourly.
  Run it manually from the Actions tab to publish a new post right away.

Run locally (Python 3, no dependencies):

```
python3 build.py && python3 -m http.server -d _site 4000
```

Set `BEAR_BLOG=https://someone.bearblog.dev` to preview with another blog's posts.
