"""Tests for functionality with fast api."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic_python_regex_validator.fast_api import RegexBody, RegexQuery

app = FastAPI()


@app.get("/foo")
def foo_get(param: RegexQuery(pattern="^foo")):
    """Test foo endpoint."""
    return param


@app.get("/foo-param")
def foo_get_with_query_param(param: RegexQuery(pattern="^foo", query_params={"alias": "aParam"})):
    """Test foo endpoint."""
    return param


@app.post("/foo")
def foo_post(param: RegexBody(pattern="^foo")):
    """Test foo endpoint."""
    return param


@app.post("/foo-param")
def foo_post_with_param(param: RegexBody(pattern="^foo", body_params={"embed": True})):
    """Test foo endpoint."""
    return param


@app.get("/bar")
def bar_get(param: RegexQuery(pattern="^bar", allow_none=True) = None):
    """Test bar endpoint."""
    return param


@app.post("/bar")
def bar_post(param: RegexBody(pattern="^bar", allow_none=True) = None):
    """Test bar endpoint."""
    return param


client = TestClient(app)


def test_correct_regex_get():
    """Tests fastapi parses the string correctly."""
    response = client.get("/foo", params={"param": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_correct_regex_get_with_alias():
    """Tests fastapi parses the string correctly."""
    response = client.get("/foo-param", params={"aParam": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_incorrect_regex_get():
    """Tests fastapi rejects the incorrect regex."""
    response = client.get("/foo", params={"param": "bar"})
    assert response.status_code == 422


def test_correct_regex_with_missing_get():
    """Tests fastapi allows none when allowed."""
    response = client.get("/bar")
    assert response.status_code == 200
    assert response.json() is None


def test_correct_regex_post():
    """Tests fastapi parses the string correctly."""
    response = client.post("/foo", json="foo")
    assert response.status_code == 200
    assert response.json() == "foo"


def test_correct_regex_post_with_embed():
    """Tests fastapi parses the string correctly."""
    response = client.post("/foo-param", json={"param": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_incorrect_regex_post():
    """Tests fastapi rejects the incorrect regex."""
    response = client.post("/foo", json={"param": "bar"})
    assert response.status_code == 422


def test_correct_regex_with_missing_post():
    """Tests fastapi allows none when allowed."""
    response = client.post("/bar")
    assert response.status_code == 200
    assert response.json() is None
