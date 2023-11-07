from agentic_edu.agents.instruments import AgentInstruments
from agentic_edu.agents.instruments import PostgresAgentInstruments
from agentic_edu.modules.db import PostgresManager
import pytest
from pytest_mock import mocker
import os


def test_agent_instruments_init():
    agent_instruments = AgentInstruments()
    assert agent_instruments.session_id is None
    assert agent_instruments.messages == []


def test_agent_instruments_sync_messages():
    agent_instruments = AgentInstruments()
    with pytest.raises(NotImplementedError):
        agent_instruments.sync_messages([])


def test_agent_instruments_make_agent_chat_file():
    agent_instruments = AgentInstruments()
    agent_instruments.session_id = "test_session"
    team_name = "test_team"
    expected_path = os.path.join(
        agent_instruments.root_dir, f"agent_chats_{team_name}.json"
    )
    assert agent_instruments.make_agent_chat_file(team_name) == expected_path


def test_postgres_agent_instruments_init():
    postgres_agent_instruments = PostgresAgentInstruments("test_db_url", "test_session")
    assert postgres_agent_instruments.session_id == "test_session"
    assert postgres_agent_instruments.messages == []


def test_postgres_agent_instruments_sync_messages():
    postgres_agent_instruments = PostgresAgentInstruments("test_db_url", "test_session")
    messages = ["message1", "message2"]
    postgres_agent_instruments.sync_messages(messages)
    assert postgres_agent_instruments.messages == messages


def test_postgres_agent_instruments_make_agent_chat_file():
    postgres_agent_instruments = PostgresAgentInstruments("test_db_url", "test_session")
    postgres_agent_instruments.session_id = "test_session"
    team_name = "test_team"
    expected_path = os.path.join(
        postgres_agent_instruments.root_dir, f"agent_chats_{team_name}.json"
    )
    assert postgres_agent_instruments.make_agent_chat_file(team_name) == expected_path


import unittest
from unittest.mock import Mock, patch, mock_open


class TestPostgresAgentInstruments(unittest.TestCase):
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    @patch("os.listdir", return_value=[])
    def test_reset_files(self, mock_listdir, mock_makedirs, mock_exists):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        instruments.reset_files()
        mock_exists.assert_called_once_with(instruments.root_dir)
        mock_makedirs.assert_called_once_with(instruments.root_dir)
        mock_listdir.assert_called_once_with(instruments.root_dir)

    def test_get_file_path(self):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        expected_path = os.path.join(instruments.root_dir, "test_file")
        self.assertEqual(instruments.get_file_path("test_file"), expected_path)

    @patch("agentic_edu.modules.db.PostgresManager")
    def test_run_sql(self, mock_manager):
        mock_manager.run_sql.return_value = "test_results"
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        instruments.db = mock_manager
        with patch("builtins.open", mock_open()) as mock_file:
            result = instruments.run_sql("SELECT * FROM test_table")
        self.assertEqual(result, "Successfully delivered results to json file")
        mock_file.assert_called_once_with(instruments.run_sql_results_file, "w")

    def test_validate_run_sql(self):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        with patch("builtins.open", mock_open(read_data="test_data")) as mock_file:
            result, message = instruments.validate_run_sql()
        self.assertTrue(result)
        self.assertEqual(message, "")
        mock_file.assert_called_once_with(instruments.run_sql_results_file, "r")

    @patch("agentic_edu.modules.file.write_file", return_value="test_result")
    def test_write_file(self, mock_write_file):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        result = instruments.write_file("test_content")
        self.assertEqual(result, "test_result")
        mock_write_file.assert_called_once_with(
            instruments.get_file_path("write_file.txt"), "test_content"
        )

    @patch("agentic_edu.modules.file.write_json_file", return_value="test_result")
    def test_write_json_file(self, mock_write_json_file):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        result = instruments.write_json_file("test_content")
        self.assertEqual(result, "test_result")
        mock_write_json_file.assert_called_once_with(
            instruments.get_file_path("write_json_file.json"), "test_content"
        )

    @patch("agentic_edu.modules.file.write_yml_file", return_value="test_result")
    def test_write_yml_file(self, mock_write_yml_file):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        result = instruments.write_yml_file("test_content")
        self.assertEqual(result, "test_result")
        mock_write_yml_file.assert_called_once_with(
            instruments.get_file_path("write_yml_file.yml"), "test_content"
        )

    @patch("agentic_edu.modules.file.write_file", return_value="test_result")
    def test_write_innovation_file(self, mock_write_file):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        result = instruments.write_innovation_file("test_content")
        self.assertEqual(
            result, "Successfully wrote innovation file. You can check my work."
        )
        mock_write_file.assert_called_once_with(
            instruments.get_file_path("0_innovation_file.json"), "test_content"
        )

    def test_validate_innovation_files(self):
        instruments = PostgresAgentInstruments("test_db_url", "test_session")
        instruments.innovation_index = 1
        with patch("builtins.open", mock_open(read_data="test_data")) as mock_file:
            result, message = instruments.validate_innovation_files()
        self.assertTrue(result)
        self.assertEqual(message, "")
        mock_file.assert_called_once_with(
            instruments.get_file_path("0_innovation_file.json"), "r"
        )


if __name__ == "__main__":
    unittest.main()
