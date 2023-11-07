import os
import dotenv
import argparse
import autogen
from agentic_edu.modules.db import PostgresManager
from agentic_edu.modules import llm
from agentic_edu.modules import orchestrator
from agentic_edu.modules import file
from agentic_edu.agents import agents
from agentic_edu.modules import embeddings

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

POSTGRES_TABLE_DEFINITIONS_CAP_REF = "TABLE_DEFINITIONS"
RESPONSE_FORMAT_CAP_REF = "RESPONSE_FORMAT"
SQL_DELIMITER = "------------"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="The prompt for the OpenAI API")
    args = parser.parse_args()

    if not args.prompt:
        print("Please provide a prompt")
        return

    raw_prompt = args.prompt

    prompt = f"Fulfill this database query: {args.prompt}."

    with PostgresManager() as db:
        db.connect_with_url(DB_URL)

        # table_definitions = db.get_table_definitions_for_prompt()
        table_definitions = db.get_table_definitions_for_prompt_MOCK()

        # map_table_name_to_table_def = db.get_table_definition_for_map_embeddings()

        # database_embedder = embeddings.DatabaseEmbedder()

        # for name, table_def in map_table_name_to_table_def.items():
        #     print(f"Adding table {name} to the database embedder")
        #     database_embedder.add_table(name, table_def)

        # print(
        #     "database_embedder.map_name_to_embeddings",
        #     database_embedder.map_name_to_embeddings,
        # )

        # print("database_embedder.", database_embedder)

        # similar_tables = database_embedder.get_similar_tables_via_embeddings(raw_prompt)

        # print("similar_tables", similar_tables)

        # return

        prompt = llm.add_cap_ref(
            prompt,
            f"Use these {POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions,
        )

        data_eng_orchestrator = agents.build_team_orchestrator("data_eng", db)

        success, data_eng_messages = data_eng_orchestrator.sequential_conversation(
            prompt
        )
        print(data_eng_messages)
        data_eng_result = data_eng_messages[-1]["content"]
        # -------------------------------------------------------

        data_viz_orchestrator = agents.build_team_orchestrator("data_viz", db)

        data_viz_prompt = f"Here is the data to report: {data_eng_result}"

        data_viz_orchestrator.broadcast_conversation(data_viz_prompt)


if __name__ == "__main__":
    main()
