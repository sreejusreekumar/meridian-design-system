import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

import meridian
from meridian import mount_meridian, static_dir, stylesheet_url


def test_static_dir_has_all_assets():
    names = {p.name for p in static_dir().iterdir()}
    assert {
        meridian.STYLESHEET,
        meridian.TOKENS_LIGHT,
        meridian.TOKENS_DARK,
        meridian.STARTER,
    } <= names


def test_tokens_parse_and_match():
    light = json.loads((static_dir() / meridian.TOKENS_LIGHT).read_text())
    dark = json.loads((static_dir() / meridian.TOKENS_DARK).read_text())
    assert set(light["color"]) == set(dark["color"])


def test_mount_serves_assets():
    app = FastAPI()
    css = mount_meridian(app)
    client = TestClient(app)

    assert css == stylesheet_url()
    assert css.startswith("/meridian/meridian.css?v=")

    r = client.get(css)
    assert r.status_code == 200
    assert "text/css" in r.headers["content-type"]
    assert ".mr-btn" in r.text

    r = client.get("/meridian/starter.html")
    assert r.status_code == 200
    assert 'href="meridian.css"' in r.text  # relative, so it resolves under the mount

    r = client.get("/meridian/meridian.tokens.dark.json")
    assert r.status_code == 200
    assert r.json()["color"]["gray-1"]["$type"] == "color"


def test_custom_mount_path():
    app = FastAPI()
    css = mount_meridian(app, path="/static/ds")
    assert css.startswith("/static/ds/meridian.css?v=")
    assert TestClient(app).get("/static/ds/meridian.css").status_code == 200
