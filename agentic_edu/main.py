import os
from agentic_edu.modules.db import PostgresManager
import agentic_edu.modules.llm

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt for the OpenAI API")
    args = parser.parse_args()

    with PostgresManager() as db:
        db.connect_with_url(DB_URL) # 'postgresql://user:secret@localhost:5432/mydatabase'
        table_definitions = db.get_table_definitions_for_prompt()

        prompt_with_table_definitions = llm.add_cap_ref(args.prompt, "Here are the table definitions:", "TABLE_DEFINITIONS", table_definitions)
        prompt_response = llm.prompt(prompt_with_table_definitions)

        sql_query = prompt_response.split('_________')[1]
        db.run_sql(sql_query)

if __name__ == '__main__':
    main()
