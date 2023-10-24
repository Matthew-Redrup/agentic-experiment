import os
import dotenv
from agentic_edu.modules.db import PostgresManager
from agentic_edu.modules.llm import add_cap_ref
import agentic_edu.modules.llm as llm
import agentic_edu.modules.orchestrator as orchestrator
import agentic_edu.modules.file as file
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
            f"Use these {POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions,
        )
        
        # build the gpt_configuration object
        # Base Configuration
        base_config = {
            "use_cache": False,
            "temperature": 0,
            "config_list": config_list_from_models(["gpt-4"]),
            "request_timeout": 120,
        }
        
        # Configuration with "run_sql"
        run_sql_config = {
            **base_config, # Inherit base configuration
            "functions": [
                {
                    "name": "run_sql",
                    "description": "Run a SQL query against the postgres database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql": {
                                "type": "string",
                                "description": "The SQL query to run",
                            }
                        },
                        "required": ["sql"],
                    },
                }
            ]
        }
        
        write_file_config = {
            **base_config, # Inherit base configuration
            "functions": [
                {
                    "name": "write_file",
                    "description": "Write a file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fname": {
                                "type": "string",
                                "description": "The name of the file to write",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content of the file to write",
                            },
                        },
                        "required": ["fname", "content"],
                    },
                }
            ],
        }
        
        # Configuration with "write_json_file"
        write_json_file_config = {
            **base_config, # Inherit base configuration
            "functions": [
                {
                    "name": "write_json_file",
                    "description": "Write a json file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fname": {
                                "type": "string",
                                "description": "The name of the file to write",
                            },
                            "json_str": {
                                "type": "string",
                                "description": "The content of the file to write",
                            },
                        },
                        "required": ["fname", "json_str"],
                    },
                }
            ],
        }
        
        write_yaml_file_config = {
            **base_config, # Inherit base configuration
            "functions": [
                {
                    "name": "write_yaml_file",
                    "description": "Write a Yaml file to the filesystem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fname": {
                                "type": "string",
                                "description": "The name of the file to write",
                            },
                            "json_str": {
                                "type": "string",
                                "description": "The content of the file to write",
                            },
                        },
                        "required": ["fname", "json_str"],
                    },
                }
            ],
        }

        # build the function map
        function_map_run_sql = {
            "run_sql": db.run_sql,  
        }
        function_map_write_file = {
            "write_file": file.write_file,
        }
        function_map_write_json_file = {
            "write_json_file": file.write_json_file,
        }
        function_map_write_yaml_file = {
            "write_yaml_file": file.write_yaml_file,
        }
        
        # create our terminate msg function
        def is_termination_msg(content):
            have_content = content.get("content", None) is not None
            if have_content and "APPROVED" in content["content"]:
                return True
            return False
        
        COMPLETION_PROMPT = "If everything looks good, respond with APPROVED"
        
        USER_PROXY_PROMPT = (
            "A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin."
            + COMPLETION_PROMPT
        )
        DATA_ENGINEER_PROMPT = (
            "A Data Engineer. You follow an approved plan. Generate the initial SQL based on the requirements provided. Send it to the Sr Data Analyst for review."
            + COMPLETION_PROMPT
        )
        SR_DATA_ANALYST_PROMPT = (
            "A Sr Data Analyst. You follow an approved plan. You run the SQL query and generate the response and send it to the product manager for final review."
            + COMPLETION_PROMPT
        )
        PRODUCT_MANAGER_PROMPT = (
            "A Product Manager. You validate the response to make sure it's correct."
            + COMPLETION_PROMPT
        )

        # create a set of agents with specific roles
        # admin user proxy agent - takes in the prompt and manages the group chat
        user_proxy = UserProxyAgent(
            name="Admin",
            system_message=USER_PROXY_PROMPT,
            code_execution_config=False,
            human_input_mode="NEVER",
            is_termination_msg=is_termination_msg,
        )

        # data engineer agent - generates the sql query
        engineer = AssistantAgent(
            name="Engineer",
            llm_config=run_sql_config,
            system_message=DATA_ENGINEER_PROMPT,
            code_execution_config=False,
            human_input_mode="NEVER",
            is_termination_msg=is_termination_msg,
        )

        # sr data analyst agent - run the sql query and generate the response
        sr_data_analyst = AssistantAgent(
            name="Sr_Data_Analyst",
            llm_config=run_sql_config,
            system_message=SR_DATA_ANALYST_PROMPT,
            code_execution_config=False,
            human_input_mode="NEVER",
            is_termination_msg=is_termination_msg,
            function_map=function_map_run_sql,
        )

        # product manager - validate the response to make sure it's correct
        product_manager = AssistantAgent(
            name="Product_Manager",
            llm_config=run_sql_config,
            system_message=PRODUCT_MANAGER_PROMPT,
            code_execution_config=False,
            human_input_mode="NEVER",
            is_termination_msg=is_termination_msg,
        )
        
        data_engineering_agents = [
            user_proxy,
            engineer,
            sr_data_analyst,
            product_manager,
        ]
        
        # create the group chat 
        data_eng_orchestrator = orchestrator.Orchestrator(
            name="Postgres Data Analytics Multi-Agent ::: Data Engineering Team",
            agents=data_engineering_agents,
        )
        
        #data_eng_orchestrator.sequential_conversation(prompt)
        
        # -------------------------------------------------------
        
        TEXT_REPORT_ANALYST_PROMPT = "Text File Report Analyst. You exclusively use the write_file function on a summarized report."
        JSON_REPORT_ANALYST_PROMPT = "Json Report Analyst. You exclusively use the write_json_file function on the report."
        YML_REPORT_ANALYST_PROMPT = "Yaml Report Analyst. You exclusively use the write_yml_file function on the report."
        
        # text report analyst = writes a summary report of the results and saves them to a local text file
        text_report_analyst = AssistantAgent(
            name="Text_Report_Analyst",
            llm_config=write_file_config,
            system_message=TEXT_REPORT_ANALYST_PROMPT,
            human_input_mode="NEVER",
            function_map=function_map_write_file,
        )
        
        # json report analyst = writes a summary report of the results and saves them to a local json file
        json_report_analyst = AssistantAgent(
            name="Json_Report_Analyst",
            llm_config=write_json_file_config,
            system_message=JSON_REPORT_ANALYST_PROMPT,
            human_input_mode="NEVER",
            function_map=function_map_write_json_file,
        )
        
        yaml_report_analyst = AssistantAgent(
            name="Yml_Report_Analyst",
            llm_config=write_yaml_file_config,
            system_message=YML_REPORT_ANALYST_PROMPT,
            human_input_mode="NEVER",
            function_map=function_map_write_yaml_file,
        )
        
        mock_data_to_report = [
            {
                "id": 1,
                "created": "2023-09-28T10:00:00",
                "updated": "2023-09-28T10:10:00",
                "authed": True,
                "plan": "Basic",
                "name": "John Doe",
                "email": "john.doe@outlook.com"
            },
            {
                "id": 2,
                "created": "2023-09-27T11:00:00",
                "updated": "2023-09-28T11:15:00",
                "authed": True,
                "plan": "Premium",
                "name": "Jane Smith",
                "email": "jane.smith@outlook.com"
            },
        ]
        
        data_viz_agents = [
            user_proxy,
            text_report_analyst,
            json_report_analyst,
            yaml_report_analyst,
        ]
        
        data_viz_orchestrator = orchestrator.Orchestrator(
            name="Postgres Data Analytics Multi-Agent ::: Data Viz Team",
            agents=data_viz_agents,
        )
        
        data_viz_prompt = f"Here is the data to report: {mock_data_to_report}"
        
        data_viz_orchestrator.broadcast_conversation(data_viz_prompt)
        
        
        

        # create a group chat and initiate a new chat
        # groupchat = GroupChat(
        #     agents=[user_proxy, engineer, sr_data_analyst, product_manager], 
        #     messages=[], 
        #     max_round=10,
        #     )
        
        # manager = GroupChatManager(groupchat=groupchat, llm_config=run_sql_config)
        
        # user_proxy.initiate_chat(manager, clear_history=True, message=prompt)
        
        
if __name__ == '__main__':
    main()
