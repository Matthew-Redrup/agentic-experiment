import unittest
from unittest.mock import patch, MagicMock, call
import os
from agentic_edu.modules import llm  # assuming the llm.py is in the same directory


class TestLLMMethods(unittest.TestCase):
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_environment_variable(self):
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "test_key")

    def test_safe_get(self):
        data = {"a": {"b": [{"c": 1}]}}
        self.assertEqual(llm.safe_get(data, "a.b.0.c"), 1)
        self.assertEqual(llm.safe_get(data, "a.b.0.d"), None)

    from unittest.mock import call  # Add this line at the top of your file

    @patch("agentic_edu.modules.llm.response_parser", return_value="test_content")
    @patch("agentic_edu.modules.llm.openai.ChatCompletion.create")
    def test_prompt(self, mock_create, mock_response_parser):
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="test_content"))]
        )
        response = llm.prompt("test_prompt")
        self.assertEqual(response, "test_content")

    def test_add_cap_ref(self):
        prompt = "Refactor this code."
        prompt_suffix = "Make it more readable using this EXAMPLE."
        cap_ref = "EXAMPLE"
        cap_ref_content = "def foo():\n    return True"
        expected = "Refactor this code. Make it more readable using this EXAMPLE.\n\nEXAMPLE\n\ndef foo():\n    return True"
        self.assertEqual(
            llm.add_cap_ref(prompt, prompt_suffix, cap_ref, cap_ref_content), expected
        )

    @patch("agentic_edu.modules.llm.tiktoken.get_encoding")
    def test_count_tokens(self, mock_get_encoding):
        mock_get_encoding.return_value = MagicMock(
            encode=MagicMock(return_value=[1, 2, 3])
        )
        self.assertEqual(llm.count_tokens("test_text"), 3)

    @patch("agentic_edu.modules.llm.count_tokens", return_value=2000)
    def test_estimate_price_and_tokens(self, mock_count_tokens):
        self.assertEqual(llm.estimate_price_and_tokens("test_text"), (0.12, 2000))


if __name__ == "__main__":
    unittest.main()
