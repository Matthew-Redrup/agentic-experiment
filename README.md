# Agentic Experiment

## Postgres Data Analytics AI Agent

This was an experiment implementing AI agents using the Autogen framework for OpenAI GPT-4. The program uses 2 types of conversation chains (sequential and broadcast) to orchestrate problem solving data questions on a postgres database provided by a user. The general problem solving flow is as follows:
- User provides a question to the agent team
- Table definitions are retrieved from the database and provided to the agent team
- Agents propose a sql query based on the question and table definitions
- Agents test the query against the database. If not successful agents troubleshoot query and propose a new query. This continues until a successful query is found.
- Results are summariesd and provided to the user.

The code was created following along with a series from [@IndyDevDan](https://www.youtube.com/@indydevdan)

- [Video 1](https://www.youtube.com/watch?v=jmDMusirPKA)
- [Video 2](https://www.youtube.com/watch?v=JjVvYDPVrAQ) 
- [Video 3](https://www.youtube.com/watch?v=4o8tymMQ5GM)
- [Video 4](https://www.youtube.com/watch?v=CKo-czvxFkY)

## Setup
```bash
git clone git@github.com:Matthew-Redrup/agentic-experiment.git
cd agentic-experiment
poetry install
```
You will need to have a Postgres Database to point the agent at.
You will need to create a .env file containing the database URL and OPENAI_API_KEY.
```
DATABASE_URL=""
OPENAI_API_KEY=""
```

## Running
```bash
poetry run start --prompt "Ask the agent questions about the database"
```