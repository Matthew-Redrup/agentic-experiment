# Agentic Experiment

## Postgres Data Analytics AI Agent

This was an experiment implementing AI agents using the Autogen framework for OpenAI GPT-4. 

The code was created following along with [Video 1](https://www.youtube.com/watch?v=jmDMusirPKA) and [Video 2](https://www.youtube.com/watch?v=JjVvYDPVrAQ) from [@IndyDevDan](https://www.youtube.com/@indydevdan).

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