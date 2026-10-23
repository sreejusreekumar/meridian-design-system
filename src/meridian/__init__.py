"""Meridian design system.

The package ships only static assets (``meridian.css``, two token JSON files and
``starter.html``). ``mount_meridian`` serves them from a FastAPI/Starlette app so
templates can link ``/meridian/meridian.css``.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from fastapi import FastAPI

try:
    __version__ = version("meridian-design-system")
except PackageNotFoundError:  # running from a checkout without install
    __version__ = "0.0.0"

DEFAULT_PATH = "/meridian"
STYLESHEET = "meridian.css"
TOKENS_LIGHT = "meridian.tokens.light.json"
TOKENS_DARK = "meridian.tokens.dark.json"
STARTER = "starter.html"

__all__ = [
    "DEFAULT_PATH",
    "STARTER",
    "STYLESHEET",
    "TOKENS_DARK",
    "TOKENS_LIGHT",
    "__version__",
    "asset_url",
    "mount_meridian",
    "static_dir",
    "stylesheet_url",
]


def static_dir() -> Path:
    """Directory holding the packaged assets."""
    return Path(__file__).parent / "static"


def asset_url(filename: str, path: str = DEFAULT_PATH) -> str:
    """URL of a packaged asset once mounted, with the version as a cache-buster."""
    return f"{path.rstrip('/')}/{filename}?v={__version__}"


def stylesheet_url(path: str = DEFAULT_PATH) -> str:
    """URL to put in ``<link rel="stylesheet" href="...">``."""
    return asset_url(STYLESHEET, path)


def mount_meridian(app: FastAPI, path: str = DEFAULT_PATH, name: str = "meridian") -> str:
    """Serve the Meridian assets on ``app`` under ``path``.

    Returns the stylesheet URL so callers can pass it straight to templates::

        from meridian import mount_meridian

        app = FastAPI()
        css = mount_meridian(app)          # "/meridian/meridian.css?v=1.0.0"
        templates.env.globals["meridian_css"] = css
    """
    from starlette.staticfiles import StaticFiles  # lazy: the app owns the dependency

    app.mount(path, StaticFiles(directory=static_dir()), name=name)
    return stylesheet_url(path)
