###############
# lint & test #
###############
format:
	poetry run black pydantic_python_regex_validator tests
	poetry run ruff check . --fix-only

lint:
	poetry run black --check pydantic_python_regex_validator tests
	poetry run ruff check .

test:
	poetry run python -m pytest --cov=pydantic_python_regex_validator --cov-report=term-missing --cov-fail-under=100 -vv --durations 5