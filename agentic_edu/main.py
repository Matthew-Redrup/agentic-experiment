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
        gpt4_config = {
            "seed": 42,  # change the seed for different trials
            "temperature": 0,
            "config_list": config_list_from_models(),
            "request_timeout": 120,
        }

        # build the function map
        # TODO: Define the function map

        # create our terminate msg function
        # TODO: Define the terminate msg function

        # create a set of agents with specific roles
        # admin user proxy agent - takes in the prompt and manages the group chat
        admin = UserProxyAgent(
            name="Admin",
            system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
            code_execution_config=False,
        )

        # data engineer agent - generates the sql query
        engineer = AssistantAgent(
            name="Engineer",
            llm_config=gpt4_config,
            system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
            Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
            If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
            ''',
        )

        # sr data analyst agent - run the sql query and generate the response
        analyst = AssistantAgent(
            name="Analyst",
            llm_config=gpt4_config,
            system_message="Analyst. You follow an approved plan. You run the SQL query and generate the response."
        )

        # product manager - validate the response to make sure it's correct
        manager = AssistantAgent(
            name="Manager",
            llm_config=gpt4_config,
            system_message="Manager. You validate the response to make sure it's correct."
        )

        # create a group chat and initiate a new chat
        groupchat = GroupChat(agents=[admin, engineer, analyst, manager], messages=[], max_round=50)
        chat_manager = GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)
        # TODO: Initiate a new chat
        
        
if __name__ == '__main__':
    main()
