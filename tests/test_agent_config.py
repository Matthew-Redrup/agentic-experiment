import unittest
import autogen
from agentic_edu.agents import agent_config
from unittest.mock import patch


class TestAgentConfig(unittest.TestCase):
    @patch("autogen.config_list_from_models")
    def test_base_config(self, mock_config_list_from_models):
        # Set up the mock to return an empty list
        mock_config_list_from_models.return_value = []

        expected_config = {
            "use_cache": False,
            "temperature": 0,
            "config_list": [],
            "request_timeout": 120,
        }
        self.assertEqual(agent_config.base_config, expected_config)

    def test_run_sql_config(self):
        expected_config = {
            **agent_config.base_config,
            "functions": [
                {
                    "name": "run_sql",
                    "description": "Run a SQL query against the postgres database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql": {
                                "type": "string",
                                "description": "The SQL query to run",
                            }
                        },
                        "required": ["sql"],
                    },
                }
            ],
        }
        self.assertEqual(agent_config.run_sql_config, expected_config)

    def test_write_file_config(self):
        expected_config = {
            **agent_config.base_config,
            "functions": [
                {
                    "name": "write_file",
                    "description": "Write a file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fname": {
                                "type": "string",
                                "description": "The name of the file to write",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content of the file to write",
                            },
                        },
                        "required": ["fname", "content"],
                    },
                }
            ],
        }
        self.assertEqual(agent_config.write_file_config, expected_config)

    def test_write_json_file_config(self):
        expected_config = {
            **agent_config.base_config,
            "functions": [
                {
                    "name": "write_json_file",
                    "description": "Write a json file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fname": {
                                "type": "string",
                                "description": "The name of the file to write",
                            },
                            "json_str": {
                                "type": "string",
                                "description": "The content of the file to write",
                            },
                        },
                        "required": ["fname", "json_str"],
                    },
                }
            ],
        }
        self.assertEqual(agent_config.write_json_file_config, expected_config)

    def test_write_yaml_file_config(self):
        expected_config = {
            **agent_config.base_config,
            "functions": [
                {
                    "name": "write_yml_file",
                    "description": "Write a yml file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fname": {
                                "type": "string",
                                "description": "The name of the file to write",
                            },
                            "json_str": {
                                "type": "string",
                                "description": "The json content of the file to write",
                            },
                        },
                        "required": ["fname", "json_str"],
                    },
                }
            ],
        }
        self.assertEqual(agent_config.write_yaml_file_config, expected_config)

    def test_write_innovation_file_config(self):
        expected_config = {
            **agent_config.base_config,
            "functions": [
                {
                    "name": "write_innovation_file",
                    "description": "Write a file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content of the file to write",
                            },
                        },
                        "required": ["content"],
                    },
                }
            ],
        }
        self.assertEqual(agent_config.write_innovation_file_config, expected_config)


if __name__ == "__main__":
    unittest.main()
