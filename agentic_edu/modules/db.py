import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


class PostgresManager:

    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.close()

    def connect_with_url(self, url):
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def upsert(self, table_name, _dict):
        columns = _dict.keys()
        values = [sql.Identifier(k) for k in _dict.values()]
        sql_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT (id) DO UPDATE SET {}").format(
            sql.Identifier(table_name),
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.SQL(',').join(map(sql.Placeholder, columns)),
            sql.SQL(',').join(sql.SQL('{} = {}').format(sql.Identifier(k), sql.Placeholder(k)) for k in columns))
        self.cur.execute(sql_query, _dict)
        self.conn.commit()

    def delete(self, table_name, _id):
        sql_query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(table_name))
        self.cur.execute(sql_query, [_id])
        self.conn.commit()

    def get(self, table_name, _id):
        sql_query = sql.SQL("SELECT * FROM {} WHERE id = %s").format(sql.Identifier(table_name))
        self.cur.execute(sql_query, [_id])
        return self.cur.fetchone()

    def get_all(self, table_name):
        sql_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        self.cur.execute(sql_query)
        return self.cur.fetchall()

    def run_sql(self, sql_query):
        self.cur.execute(sql_query)
        self.conn.commit()

    def get_table_definitions(self, table_name):
        sql_query = sql.SQL("SELECT column_name, data_type, character_maximum_length "
                            "FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s").format(sql.Identifier(table_name))
        self.cur.execute(sql_query, [table_name])
        return self.cur.fetchall()

    def get_all_table_names(self):
        self.cur.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='public'")
        return self.cur.fetchall()

    def get_table_definitions_for_prompt(self):
        table_names = self.get_all_table_names()
        table_definitions = []
        for table_name in table_names:
            table_definitions.append({"table_name": table_name, "table_definition": self.get_table_definitions(table_name)})
        return "\n".join([str(t) for t in table_definitions])