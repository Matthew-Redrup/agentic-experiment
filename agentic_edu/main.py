import os
from agentic_edu.modules.db import PostgresManager
import agentic_edu.modules.llm

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def main():
    # parse prompt param using arg parse
    
    with PostgresManager() as db:
        db.connect_with_url(DB_URL) # 'postgresql://user:secret@localhost:5432/mydatabase'
        users_table = db.get_all("users")
        
        print("users_table", users_table)
    
        # call db_manager.get_table_definition_for_prompt() to get tables in prompt ready form
    
        # create two blank calls to llm.add_cap_ref() that update our current prompt passed in from cli
    
        # call llm.prompt to get a prompt_response variable
    
        # parse sql response from prompt_response using SQL_QUERY_DELIMITER '_________'
    
        # call db_manager.run_sql() with the parsed sql
    
    pass

if __name__ == '__main__':
    main()