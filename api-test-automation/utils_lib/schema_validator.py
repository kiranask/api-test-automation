from jsonschema import validate, ValidationError
import pytest

def validate_response_schema(response_json, schema):
    """
    Validates API response against a JSON Schema.
    Ensures contract is not broken when APIs evolve.
    Fails the test if schema does not match.
    """
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")
