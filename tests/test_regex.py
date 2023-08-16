"""Tests the functionality of the Regex validator."""
from platform import python_version
from typing import Optional

import pydantic
import pytest

from pydantic_python_regex_validator.regex import Regex

if python_version()[:3] == "3.8":
    from typing_extensions import Annotated
else:
    from typing import Annotated


class TestLookAroundRegex:
    """Tests functionality using a lookaround regex."""

    class Model(pydantic.BaseModel):
        """Test model."""

        field: Annotated[
            str,
            Regex(
                r"^P(?!$)(\d+(?:\.\d+)?Y)?(\d+(?:\.\d+)?M)?(\d+(?:\.\d+)?W)?(\d+(?:\.\d+)?D)"
                r"?(T(?=\d)(\d+(?:\.\d+)?H)?(\d+(?:\.\d+)?M)?(\d+(?:\.\d+)?S)?)?$",
            ),
        ]

    @pytest.mark.parametrize("value", ["PT30M", "PT60M", "PT1H", "P1D", "P1M"])
    def test_model_validate_true(self, value):
        """Tests validating with a valid string."""
        assert self.Model(field=value).field == value

    @pytest.mark.parametrize("value", ["foo", "123", "BAR", "PTJ30M"])
    def test_model_validate_false(self, value):
        """Tests an exception is raised for an invalid string."""
        with pytest.raises(pydantic.ValidationError):
            self.Model(field=value)

    def test_field_regex_in_schema(self):
        """Tests the pattern appears in the schema."""
        schema = self.Model(field="PT30M").model_json_schema()
        assert (
            schema["properties"]["field"]["pattern"]
            == r"^P(?!$)(\d+(?:\.\d+)?Y)?(\d+(?:\.\d+)?M)?(\d+(?:\.\d+)?W)?(\d+(?:\.\d+)?D)"
            r"?(T(?=\d)(\d+(?:\.\d+)?H)?(\d+(?:\.\d+)?M)?(\d+(?:\.\d+)?S)?)?$"
        )


class TestRegularRegex:
    """Tests functionality with a regular regex."""

    class Model(pydantic.BaseModel):
        """Test Model."""

        field: Annotated[str, Regex(r"^foo")]

    @pytest.mark.parametrize("value", ["foo", "foobar", "foo123", "foo!"])
    def test_model_validate_true(self, value):
        """Tests validating with a valid string."""
        assert self.Model(field=value).field == value

    @pytest.mark.parametrize("value", ["bar", "barfoo", "1foo", "28437"])
    def test_model_validate_false(self, value):
        """Tests an exception is raised for an invalid string."""
        with pytest.raises(pydantic.ValidationError):
            self.Model(field=value)

    def test_field_regex_in_schema(self):
        """Tests the pattern appears in the schema."""
        schema = self.Model(field="foo").model_json_schema()
        assert schema["properties"]["field"]["pattern"] == r"^foo"


class TestRegexWithNone:
    """Tests functionality with a regular regex, allowing the field to be None."""

    class Model(pydantic.BaseModel):
        """Test Model."""

        field: Annotated[Optional[str], Regex(r"^foo", allow_none=True)]

    @pytest.mark.parametrize("value", ["foo", "foobar", "foo123", "foo!", None])
    def test_model_validate_true(self, value):
        """Tests validating with a valid string."""
        assert self.Model(field=value).field == value

    @pytest.mark.parametrize("value", ["bar", "barfoo", "1foo", "28437"])
    def test_model_validate_false(self, value):
        """Tests an exception is raised for an invalid string."""
        with pytest.raises(pydantic.ValidationError):
            self.Model(field=value)

    def test_field_regex_in_schema(self):
        """Tests the pattern appears in the schema."""
        schema = self.Model(field="foo").model_json_schema()
        assert schema["properties"]["field"]["pattern"] == r"^foo"
