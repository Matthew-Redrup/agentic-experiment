import unittest
from agentic_edu.agents.agents import (
    build_data_eng_team,
    build_data_viz_team,
    build_scrum_master_team,
    build_insights_team,
)
from agentic_edu.agents.instruments import PostgresAgentInstruments
from unittest.mock import patch, MagicMock


class TestAgents(unittest.TestCase):
    @patch("agentic_edu.agents.instruments.PostgresAgentInstruments.run_sql")
    def test_build_data_eng_team(self, mock_run_sql):
        # Set up the mock
        mock_run_sql.return_value = MagicMock()

        # Create the instruments with the mocked method
        db_url = "postgresql://username:password@localhost:5432/mydatabase"
        session_id = "test_session"
        self.instruments = PostgresAgentInstruments(db_url, session_id)

        # Now when you call run_sql, it will use the mock instead of the real method
        team = build_data_eng_team(self.instruments)
        self.assertEqual(len(team), 3)
        self.assertEqual(team[0].name, "Admin")
        self.assertEqual(team[1].name, "Engineer")
        self.assertEqual(team[2].name, "Sr_Data_Analyst")

    @patch("agentic_edu.agents.instruments.PostgresAgentInstruments.run_sql")
    def test_build_data_viz_team(self, mock_run_sql):
        # Set up the mock
        mock_run_sql.return_value = MagicMock()

        # Create the instruments with the mocked method
        db_url = "postgresql://username:password@localhost:5432/mydatabase"
        session_id = "test_session"
        self.instruments = PostgresAgentInstruments(db_url, session_id)

        team = build_data_viz_team(self.instruments)
        self.assertEqual(len(team), 4)
        self.assertEqual(team[0].name, "Admin")
        self.assertEqual(team[1].name, "Text_Report_Analyst")
        self.assertEqual(team[2].name, "Json_Report_Analyst")
        self.assertEqual(team[3].name, "Yml_Report_Analyst")

    @patch("agentic_edu.agents.instruments.PostgresAgentInstruments.run_sql")
    def test_build_scrum_master_team(self, mock_run_sql):
        # Set up the mock
        mock_run_sql.return_value = MagicMock()

        # Create the instruments with the mocked method
        db_url = "postgresql://username:password@localhost:5432/mydatabase"
        session_id = "test_session"
        self.instruments = PostgresAgentInstruments(db_url, session_id)

        team = build_scrum_master_team(self.instruments)
        self.assertEqual(len(team), 2)
        self.assertEqual(team[0].name, "Admin")
        self.assertEqual(team[1].name, "Scrum_Master")

    @patch("agentic_edu.agents.instruments.PostgresAgentInstruments.run_sql")
    def test_build_insights_team(self, mock_run_sql):
        # Set up the mock
        mock_run_sql.return_value = MagicMock()

        # Create the instruments with the mocked method
        db_url = "postgresql://username:password@localhost:5432/mydatabase"
        session_id = "test_session"
        self.instruments = PostgresAgentInstruments(db_url, session_id)

        team = build_insights_team(self.instruments)
        self.assertEqual(len(team), 3)
        self.assertEqual(team[0].name, "Admin")
        self.assertEqual(team[1].name, "Insights")
        self.assertEqual(team[2].name, "Insights_Data_Reporter")


if __name__ == "__main__":
    unittest.main()
