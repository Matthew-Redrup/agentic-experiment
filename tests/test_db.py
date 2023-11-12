import unittest
from unittest.mock import patch, MagicMock
from agentic_edu.modules.db import PostgresManager


class TestPostgresManager(unittest.TestCase):
    @patch("psycopg2.connect")
    def setUp(self, mock_connect):
        # Mock the connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cur = MagicMock()

        # Set the return values
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cur

        # Create the PostgresManager instance
        self.manager = PostgresManager()
        self.manager.connect_with_url(
            "postgresql://username:password@localhost:5432/mydatabase"
        )

    def test_run_sql(self):
        # Set up the mock
        self.mock_cur.description = [("column1",), ("column2",)]
        self.mock_cur.fetchall.return_value = [("value1", "value2")]

        # Run the method
        result = self.manager.run_sql("SELECT * FROM table")

        # Check the result
        expected_result = '[\n    {\n        "column1": "value1",\n        "column2": "value2"\n    }\n]'
        self.assertEqual(result, expected_result)

    def test_close(self):
        self.manager.close()
        self.mock_cur.close.assert_called_once()
        self.mock_conn.close.assert_called_once()

    @patch("agentic_edu.modules.db.PostgresManager.get_all_table_names")
    def test_get_table_definitions_for_prompt(self, mock_get_all_table_names):
        mock_get_all_table_names.return_value = ["table1", "table2"]
        self.mock_cur.fetchall.return_value = [
            ("table1", 1, "column1", "integer"),
            ("table2", 2, "column2", "varchar"),
        ]
        result = self.manager.get_table_definitions_for_prompt()
        expected_result = (
            "CREATE TABLE table1 (\ncolumn1 integer,\ncolumn2 varchar\n);\n\n"
            "CREATE TABLE table2 (\ncolumn1 integer,\ncolumn2 varchar\n);"
        )
        self.assertEqual(result, expected_result)

    def test_get_all_table_names(self):
        self.mock_cur.fetchall.return_value = [("table1",), ("table2",)]
        result = self.manager.get_all_table_names()
        self.assertEqual(result, ["table1", "table2"])

    def test_get_table_definition(self):
        self.mock_cur.fetchall.return_value = [
            ("table1", 1, "column1", "integer"),
            ("table1", 2, "column2", "varchar"),
        ]
        result = self.manager.get_table_definition("table1")
        self.assertEqual(
            result, "CREATE TABLE table1 (\ncolumn1 integer,\ncolumn2 varchar\n);"
        )

    @patch("agentic_edu.modules.db.PostgresManager.get_all_table_names")
    def test_get_table_definition_map_for_embeddings(self, mock_get_all_table_names):
        mock_get_all_table_names.return_value = ["table1", "table2"]
        self.mock_cur.fetchall.return_value = [
            ("table1", 1, "column1", "integer"),
            ("table1", 2, "column2", "varchar"),
        ]
        result = self.manager.get_table_definition_map_for_embeddings()
        self.assertEqual(
            result,
            {
                "table1": "CREATE TABLE table1 (\ncolumn1 integer,\ncolumn2 varchar\n);",
                "table2": "CREATE TABLE table2 (\ncolumn1 integer,\ncolumn2 varchar\n);",
            },
        )

    def test_get_related_tables(self):
        self.mock_cur.fetchall.side_effect = [[("table2",)], [("table3",)]]
        result = self.manager.get_related_tables(["table1"])
        self.assertEqual(sorted(result), sorted(["table2", "table3"]))


if __name__ == "__main__":
    unittest.main()
