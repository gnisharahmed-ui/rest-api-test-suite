"""
JSON schema validation utility using jsonschema.
Provides clean assertion helpers for API response validation.
"""
import json
import logging
from pathlib import Path
from jsonschema import validate, ValidationError

log = logging.getLogger(__name__)

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"


def load_schema(schema_file: str) -> dict:
    """Load a JSON schema file from the schemas directory."""
    schema_path = SCHEMA_DIR / schema_file
    with open(schema_path, "r") as f:
        return json.load(f)


def assert_schema(response_json: dict, schema_file: str):
    """
    Assert that response_json matches the given schema file.
    Raises AssertionError with a clear message on failure.
    """
    schema = load_schema(schema_file)
    try:
        validate(instance=response_json, schema=schema)
        log.info("Schema validation passed: %s", schema_file)
    except ValidationError as e:
        raise AssertionError(
            f"Schema validation FAILED for '{schema_file}':\n"
            f"  Path: {' -> '.join(str(p) for p in e.absolute_path)}\n"
            f"  Error: {e.message}\n"
            f"  Response: {json.dumps(response_json, indent=2)}"
        ) from e


def assert_response(response, expected_status: int, schema_file: str = None):
    """
    Assert HTTP status code and optionally validate response schema.
    """
    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, got {response.status_code}\n"
        f"Body: {response.text}"
    )

    if schema_file:
        assert_schema(response.json(), schema_file)
