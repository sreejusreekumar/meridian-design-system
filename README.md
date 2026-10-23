# Meridian design system

Tokens and components as one plain CSS file, no build step, packaged so every
FastAPI app in the family serves the same copy.

Assets shipped under `meridian/static/`:

| File | Purpose |
| --- | --- |
| `meridian.css` | Semantic + primitive tokens (light and dark) and the `mr-` components |
| `meridian.tokens.light.json`, `meridian.tokens.dark.json` | The same tokens in W3C design-token JSON, for tooling |
| `starter.html` | Reference page showing the app shell built on Meridian |

## Install in an app

Add the package as a git dependency pinned to a tag, then re-lock:

```toml
# pyproject.toml
[project]
dependencies = [
    "meridian-design-system",
]

[tool.uv.sources]
meridian-design-system = { git = "https://github.com/sreejusreekumar/meridian-design-system.git", tag = "v1.0.0" }
```

```sh
uv lock && uv sync
```

Docker images need `git` installed for `uv sync --frozen` to fetch it. The
trip-assistant image already does this for its `flights` dependency.

## Use in an app

One import and one call:

```python
from fastapi import FastAPI
from meridian import mount_meridian

app = FastAPI()
meridian_css = mount_meridian(app)  # serves /meridian/*, returns "/meridian/meridian.css?v=1.0.0"
templates.env.globals["meridian_css"] = meridian_css
```

```html
<link rel="stylesheet" href="{{ meridian_css }}">
<link rel="stylesheet" href="/static/app.css">  <!-- app CSS always comes after Meridian -->
```

Set `<html data-theme="light|dark">` to force a theme, or omit it to follow the OS.

`mount_meridian(app, path="/other")` mounts elsewhere. `meridian.static_dir()`
gives the asset directory for anything that wants to copy or inline the files.

## The rules

These keep three apps looking like one family.

1. **Apps never override `mr-` classes.** If a component needs to change, change
   it here and release a new tag.
2. **Apps may redefine tokens, on their own root only.** Put overrides in app CSS
   after the Meridian stylesheet:
   ```css
   :root { --accent-9: #0f766e; }
   ```
   Redefine semantic tokens (`--accent-*`, `--text-*`, `--bg-*`, `--space-*`) rather
   than primitives.
3. **App-specific CSS is layered after Meridian** and is built from Meridian
   tokens, the way `starter.html` builds its `.app`, `.main` and `.stats`.
4. **Upgrade by changing one line.** Bump the `tag` in `[tool.uv.sources]`, run
   `uv lock`, and check the changelog for anything that needs attention.

## Releasing a change

1. Edit the assets under `src/meridian/static/`.
2. Add an entry to `CHANGELOG.md` and bump `version` in `pyproject.toml`.
3. `uv run pytest`
4. Commit, then `git tag vX.Y.Z && git push --tags`.

Each app upgrades when it chooses by pointing at the new tag.

## Development

```sh
uv sync            # installs the dev group (fastapi, httpx, pytest, ruff)
uv run pytest
uv run ruff check .
```
