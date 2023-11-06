import unittest
import psycopg2
import pytest
from unittest.mock import Mock, patch
from agentic_edu.modules.db import PostgresManager


class TestPostgresManager(unittest.TestCase):
    @patch("psycopg2.connect")
    def test_connect_with_url(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()

        # Act
        manager.connect_with_url(url)

        # Assert
        mock_connect.assert_called_once_with(url)
        mock_conn.cursor.assert_called_once()
        self.assertEqual(manager.conn, mock_conn)
        self.assertEqual(manager.cur, mock_cur)

    @patch("psycopg2.connect")
    def test_upsert(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        table_name = "test_table"
        _dict = {"id": 1, "name": "Test"}

        # Act
        manager.upsert(table_name, _dict)

        # Assert
        mock_cur.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch("psycopg2.connect")
    def test_delete(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        table_name = "test_table"
        _id = 1

        # Act
        manager.delete(table_name, _id)

        # Assert
        mock_cur.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch("psycopg2.connect")
    def test_get(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        table_name = "test_table"
        _id = 1

        # Act
        manager.get(table_name, _id)

        # Assert
        mock_cur.execute.assert_called_once()
        mock_cur.fetchone.assert_called_once()

    @patch("psycopg2.connect")
    def test_get_all(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        table_name = "test_table"

        # Act
        manager.get_all(table_name)

        # Assert
        mock_cur.execute.assert_called_once()
        mock_cur.fetchall.assert_called_once()

    @patch("psycopg2.connect")
    def test_run_sql(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        sql = "SELECT * FROM test_table"

        # Act
        manager.run_sql(sql)

        # Assert
        mock_cur.execute.assert_called_once_with(sql)
        mock_cur.fetchall.assert_called_once()

    @patch("psycopg2.connect")
    def test_run_sql_with_invalid_sql(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()

        def mock_execute(sql):
            if sql == "INVALID SQL":
                raise psycopg2.Error("Invalid SQL command")

        mock_cur.execute.side_effect = mock_execute
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        sql = "INVALID SQL"

        # Act and Assert
        with self.assertRaises(psycopg2.Error):
            manager.run_sql(sql)

    @patch("psycopg2.connect")
    def test_run_sql_with_fetchall_exception(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.side_effect = psycopg2.Error("fetchall error")
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        sql = "SELECT * FROM test_table"

        # Act and Assert
        with self.assertRaises(psycopg2.Error):
            manager.run_sql(sql)

    @patch("psycopg2.connect")
    def test_run_sql_with_no_results(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.return_value = []
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        sql = "SELECT * FROM empty_table"

        # Act
        result = manager.run_sql(sql)

        # Assert
        self.assertEqual(result, [])

    @patch("psycopg2.connect")
    def test_run_sql_with_non_select_command(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        url = "postgresql://user:pass@localhost:5432/dbname"
        manager = PostgresManager()
        manager.connect_with_url(url)
        sql = "UPDATE test_table SET column = value"

        # Act
        result = manager.run_sql(sql)

        # Assert
        mock_cur.execute.assert_called_once_with(sql)
        mock_conn.commit.assert_called_once()
        self.assertIsNone(result)

    @patch("psycopg2.connect")
    def test_run_transaction_success(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        manager = PostgresManager()
        manager.connect_with_url("postgresql://user:pass@localhost:5432/dbname")
        sql_commands = [
            "UPDATE test_table SET column1 = value1",
            "UPDATE test_table SET column2 = value2",
        ]

        # Act
        manager.run_transaction(sql_commands)

        # Assert
        assert (
            mock_cur.execute.call_count == len(sql_commands) + 1
        )  # +1 for the BEGIN command
        mock_conn.commit.assert_called_once()

    @patch("psycopg2.connect")
    def test_run_transaction_failure(self, mock_connect):
        # Arrange
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        manager = PostgresManager()
        manager.connect_with_url("postgresql://user:pass@localhost:5432/dbname")
        sql_commands = ["UPDATE test_table SET column1 = value1", "INVALID SQL"]

        def mock_execute(sql):
            if sql == "INVALID SQL":
                raise psycopg2.Error("Invalid SQL command")

        mock_cur.execute.side_effect = mock_execute

        # Act and Assert
        with pytest.raises(psycopg2.Error):
            manager.run_transaction(sql_commands)

        mock_conn.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
