from typing import Annotated, Optional

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

from pydantic_python_regex_validator.regex import Regex

app = FastAPI()

@app.get("/foo")
def foo(param: Annotated[str, Query(), Regex("^foo")]):
    return param


@app.get("/bar")
def bar(param: Annotated[Optional[str], Query(), Regex("^bar", allow_none=True)] = None):
    return param


client = TestClient(app)


def test_correct_regex():
    response = client.get("/foo", params={"param": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_incorrect_regex():
    response = client.get("/foo", params={"param": "bar"})
    assert response.status_code == 422


def test_correct_regex_with_missing():
    response = client.get("/bar")
    assert response.status_code == 200
    assert response.json() is None
