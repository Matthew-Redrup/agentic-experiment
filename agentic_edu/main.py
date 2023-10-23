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
        db.connect_with_url(DB_URL)
        
        table_definitions = db.get_table_definitions_for_prompt()
        
        prompt = add_cap_ref(
            prompt,
            f"Use these [{POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions,
        )
        
        # build the gpt_configuration object
        
        # build the function map
        
        # create our terminate msg function
        
        # create a set of agents with specific roles
            # admin user proxy agent - takes in the prompt and manages the group chat
            # data engineer agent - generates the sql query
            # sr data analyst agent - run the sql query and generate the response
            # product manager - validate the response to make sure it's correct
        
        # create a group chat and initiate a new chat
        
        
if __name__ == '__main__':
    main()
