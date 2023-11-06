import os
import pytest
from unittest.mock import patch, MagicMock
from agentic_edu.modules.llm import safe_get, response_parser, prompt, add_cap_ref


def test_safe_get():
    data = {"a": {"b": [{"c": 1}]}}
    assert safe_get(data, "a.b.0.c") == 1
    assert safe_get(data, "a.b") == [{"c": 1}]
    assert safe_get(data, "a") == {"b": [{"c": 1}]}
    with pytest.raises(KeyError):
        safe_get(data, "a.b.1.c")


def test_response_parser():
    response = {"choices": [{"message": {"content": "test content"}}]}
    assert response_parser(response) == "test content"


@patch("openai.ChatCompletion.create")
def test_prompt(mock_create):
    mock_create.return_value = {"choices": [{"message": {"content": "test content"}}]}
    assert prompt("test prompt") == "test content"


def test_add_cap_ref():
    prompt_str = "Refactor this code."
    prompt_suffix = "Make it more readable using this EXAMPLE."
    cap_ref = "EXAMPLE"
    cap_ref_content = "def foo():\n    return True"
    expected = "Refactor this code. Make it more readable using this EXAMPLE.\n\nEXAMPLE\n\ndef foo():\n    return True"
    assert add_cap_ref(prompt_str, prompt_suffix, cap_ref, cap_ref_content) == expected
