# AGENTS.md

## Cursor Cloud specific instructions

This repo is a single **Jekyll static site** (personal blog, deployed via GitHub Pages). There is no backend, database, or other service — the only service is the Jekyll dev server.

### Toolchain / environment
- Ruby is installed system-wide (Ruby 3.2 via apt). Gems are **not** installed to the system dir; instead `GEM_HOME` is set to `$HOME/.gem` (configured in `~/.bashrc`) so `bundle`/`gem` work without `sudo`. This is already in place; you do not need to re-run it.
- Dependencies are managed by Bundler (`Gemfile` / `Gemfile.lock`). The startup update script runs `bundle install`.

### Run the dev server
- Serve locally with auto-regeneration: `bundle exec jekyll serve --host 0.0.0.0 --port 4000` (serves at `http://127.0.0.1:4000/`).
- One-off build: `bundle exec jekyll build` (output in `_site/`, which is gitignored).
- There are no lint or automated test suites in this repo. `bundle exec jekyll build` is the effective "does it compile" check.

### Gotchas
- `_config.yml` is **not** hot-reloaded by `jekyll serve`; restart the server after editing it. Content files under `_posts/`, `*.md`, and `assets/` are auto-regenerated on save.
- The About page is served at `/about/` (from `about_me.md`), not `/about_me.html`.
- Blog post URLs follow `categories` + date, e.g. a post with `categories: tech opinion` dated 2025-11-16 is at `/tech/opinion/2025/11/16/<slug>.html`.
