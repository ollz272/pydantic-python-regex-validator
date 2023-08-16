"""Tests for functionality with fast api."""
from platform import python_version
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

from pydantic_python_regex_validator.regex import Regex

if python_version()[:3] == "3.8":
    from typing_extensions import Annotated
else:
    from typing import Annotated

app = FastAPI()


@app.get("/foo")
def foo(param: Annotated[str, Query(), Regex("^foo")]):
    """Test foo endpoint."""
    return param


@app.get("/bar")
def bar(param: Annotated[Optional[str], Query(), Regex("^bar", allow_none=True)] = None):
    """Test bar endpoint."""
    return param


client = TestClient(app)


def test_correct_regex():
    """Tests fastapi parses the string correctly."""
    response = client.get("/foo", params={"param": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_incorrect_regex():
    """Tests fastapi rejects the incorrect regex."""
    response = client.get("/foo", params={"param": "bar"})
    assert response.status_code == 422


def test_correct_regex_with_missing():
    """Tests fastapi allows none when allowed."""
    response = client.get("/bar")
    assert response.status_code == 200
    assert response.json() is None
