import json
import os
import pytest
import yaml
from agentic_edu.modules.file import write_file, write_json_file, write_yaml_file


def test_write_file():
    # Arrange
    fname = "test.txt"
    content = "Hello, World!"

    # Act
    write_file(fname, content)

    # Assert
    with open(fname, "r") as f:
        assert f.read() == content

    # Cleanup
    os.remove(fname)


def test_write_json_file():
    # Arrange
    fname = "test.json"
    json_str = '{"key": "value"}'

    # Act
    write_json_file(fname, json_str)

    # Assert
    with open(fname, "r") as f:
        assert json.load(f) == json.loads(json_str)

    # Cleanup
    os.remove(fname)


def test_write_yaml_file():
    # Arrange
    fname = "test.yaml"
    json_str = '{"key": "value"}'

    # Act
    write_yaml_file(fname, json_str)

    # Assert
    with open(fname, "r") as f:
        assert yaml.safe_load(f) == json.loads(json_str)

    # Cleanup
    os.remove(fname)


def test_write_yaml_file_with_invalid_json():
    # Arrange
    fname = "test.yaml"
    json_str = "invalid json"

    # Act and Assert
    with pytest.raises(json.decoder.JSONDecodeError):
        write_yaml_file(fname, json_str)
