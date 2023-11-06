import psycopg2
from psycopg2.sql import SQL, Identifier
from typing import Dict


class PostgresManager:
    def __init__(self):
        """
        Initialize a new instance of the PostgresManager class.
        """
        self.conn = None
        self.cur = None

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        The with statement will bind this method’s return value to the target(s) specified in the as clause of the statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object.
        The parameters describe the exception that caused the context to be exited.
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def connect_with_url(self, url: str) -> None:
        """
        Connect to the PostgreSQL database.

        Args:
            url (str): The connection url.
        """
        try:
            self.conn = psycopg2.connect(url)
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def upsert(self, table_name: str, _dict: Dict) -> None:
        """
        Insert or update a row in the table.

        Args:
            table_name (str): The name of the table.
            _dict (Dict): The data to insert or update.
        """
        columns = _dict.keys()
        values = [SQL("%s")] * len(columns)
        upsert_stmt = SQL(
            "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT (id) DO UPDATE SET {}"
        ).format(
            Identifier(table_name),
            SQL(", ").join(map(Identifier, columns)),
            SQL(", ").join(values),
            SQL(", ").join(
                [
                    SQL("{} = EXCLUDED.{}").format(Identifier(k), Identifier(k))
                    for k in columns
                ]
            ),
        )
        try:
            self.cur.execute(upsert_stmt, list(_dict.values()))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error executing upsert: {e}")
            self.conn.rollback()
            raise

    def delete(self, table_name, _id):
        """
        Delete a row from the table.

        Args:
            table_name (str): The name of the table.
            _id (int): The id of the row to delete.
        """
        delete_stmt = SQL("DELETE FROM {} WHERE id = %s").format(Identifier(table_name))
        self.cur.execute(delete_stmt, (_id,))
        self.conn.commit()

    def get(self, table_name, _id):
        """
        Get a row from the table.

        Args:
            table_name (str): The name of the table.
            _id (int): The id of the row to get.

        Returns:
            tuple: The row data.
        """
        select_stmt = SQL("SELECT * FROM {} WHERE id = %s").format(
            Identifier(table_name)
        )
        self.cur.execute(select_stmt, (_id,))
        return self.cur.fetchone()

    def get_all(self, table_name):
        """
        Get all rows from the table.

        Args:
            table_name (str): The name of the table.

        Returns:
            list: The list of all rows.
        """
        select_all_stmt = SQL("SELECT * FROM {}").format(Identifier(table_name))
        self.cur.execute(select_all_stmt)
        return self.cur.fetchall()

    def run_sql(self, sql):
        """
        Execute a SQL command and commit the transaction.

        Args:
            sql (str): The SQL command to execute.

        Returns:
            list: The result of the SQL command if it is a SELECT command.
            None: If the SQL command is not a SELECT command.

        Raises:
            psycopg2.Error: If an error occurs while executing the SQL command.
        """
        self.cur.execute(sql)
        self.conn.commit()
        if sql.strip().upper().startswith("SELECT"):
            return self.cur.fetchall()
        else:
            return None

    def run_transaction(self, sql_commands):
        """
        Run multiple SQL commands in a single transaction.

        Args:
            sql_commands (list): The list of SQL commands to run.

        Raises:
            psycopg2.Error: If an error occurs while executing the SQL commands.
        """
        try:
            # Start the transaction
            self.cur.execute("BEGIN")

            # Execute each SQL command
            for sql in sql_commands:
                self.cur.execute(sql)

            # Commit the transaction
            self.conn.commit()
        except psycopg2.Error as e:
            # If an error occurs, rollback the transaction
            self.conn.rollback()
            print(f"Error executing transaction: {e}")
            raise

    def get_table_definition(self, table_name):
        get_def_stmt = """
        SELECT pg_class.relname as tablename,
            pg_attribute.attnum,
            pg_attribute.attname,
            format_type(atttypid, atttypmod)
        FROM pg_class
        JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
        JOIN pg_attribute ON pg_attribute.attrelid = pg_class.oid
        WHERE pg_attribute.attnum > 0
            AND pg_class.relname = %s
            AND pg_namespace.nspname = 'public' -- Assuming you're interested in public schema
        """
        self.cur.execute(get_def_stmt, (table_name,))
        rows = self.cur.fetchall()
        create_table_stmt = "CREATE TABLE {} (\n".format(table_name)
        for row in rows:
            create_table_stmt += "{} {},\n".format(row[2], row[3])
        create_table_stmt = create_table_stmt.rstrip(",\n") + "\n);"
        return create_table_stmt

    def get_all_table_names(self):
        get_all_tables_stmt = (
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
        )
        self.cur.execute(get_all_tables_stmt)
        return [row[0] for row in self.cur.fetchall()]

    def get_table_definitions_for_prompt(self):
        table_names = self.get_all_table_names()
        definitions = []
        for table_name in table_names:
            definitions.append(self.get_table_definition(table_name))
        return "\n\n".join(definitions)
