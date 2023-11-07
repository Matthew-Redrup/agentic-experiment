import unittest
from unittest.mock import mock_open, patch, call
import json
import yaml
from agentic_edu.modules import file  # assuming the file.py is in the same directory


class TestFileMethods(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_write_file(self, mock_file):
        file.write_file("test.txt", "Hello, World!")
        mock_file.assert_called_once_with("test.txt", "w")
        mock_file().write.assert_called_once_with("Hello, World!")

    from unittest.mock import call  # Add this line at the top of your file

    @patch("builtins.open", new_callable=mock_open)
    def test_write_json_file(self, mock_file):
        json_str = '{"key": "value"}'
        file.write_json_file("test.json", json_str)
        mock_file.assert_called_once_with("test.json", "w")
        calls = [
            call("{"),
            call("\n    "),
            call('"key"'),
            call(": "),
            call('"value"'),
            call("\n"),
            call("}"),
        ]
        mock_file().write.assert_has_calls(calls, any_order=True)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_yml_file(self, mock_file):
        json_str = '{"key": "value"}'
        file.write_yml_file("test.yml", json_str)
        mock_file.assert_called_once_with("test.yml", "w")
        calls = [call("key"), call(":"), call(" "), call("value"), call("\n")]
        mock_file().write.assert_has_calls(calls, any_order=True)


if __name__ == "__main__":
    unittest.main()
