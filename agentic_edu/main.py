import os
import dotenv
from agentic_edu.modules.db import PostgresManager
from agentic_edu.modules.llm import add_cap_ref
import agentic_edu.modules.llm as llm
import argparse
from autogen import (
    AssistantAgent,
    UserProxyAgent,
    GroupChat,
    GroupChatManager,
    config_list_from_json,
    config_list_from_models,
)

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

POSTGRES_TABLE_DEFINITIONS_CAP_REF = "TABLE_DEFINITIONS"
#POSTGRES_SQL_QUERY_CAP_REF = "SQL_QUERY"
RESPONSE_FORMAT_CAP_REF = "RESPONSE_FORMAT"
SQL_DELIMITER = "------------"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="The prompt for the OpenAI API")
    args = parser.parse_args()
    
    if not args.prompt:
        print("Please provide a prompt")
        return
    
    prompt = f"Fulfill this database query: {args.prompt}."

    with PostgresManager() as db:
        
        print("prompt v1", prompt)
        
        db.connect_with_url(DB_URL)
        
        table_definitions = db.get_table_definitions_for_prompt()
        print("table_definitions", table_definitions)
        
        prompt = add_cap_ref(
            prompt,
            f"Use these [{POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions,
        )
        
        print("prompt v2", prompt)
        
        prompt = add_cap_ref(
            prompt, 
            f"\n\nRespond in this format {RESPONSE_FORMAT_CAP_REF}. Replace the text between <> with it's request. I need to be able to easily parse the sql query from your response.",
            RESPONSE_FORMAT_CAP_REF,
            f"""<explanation of the sql query>
{SQL_DELIMITER}
<sql query exclusively as raw text>""",
        )
        
        print("\n\n----------- PROMPT -----------")
        print("prompt v3", prompt)
        
        prompt_response = llm.prompt(prompt)
        
        print("\n\n----------- PROMPT RESPONSE -----------")
        print("prompt_response", prompt_response)

        sql_query = prompt_response.split(SQL_DELIMITER)[1].strip()
        
        print("\n\n----------- PARSED SQL QUERY -----------")
        print("sql_query", sql_query)
        
        result = db.run_sql(sql_query)
        
        print("\n\n-========== POSTGRES DATA ANALYTICS AI AGENT RESPONSE ==========-")
        
        print(result)

if __name__ == '__main__':
    main()
