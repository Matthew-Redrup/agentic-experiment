# Agentic Experiment
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Python Versions](https://img.shields.io/pypi/pyversions/poetry-core)](https://pypi.org/project/poetry-core/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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


## Installation
To install the project, follow these steps:
1. Clone the repository:
```bash
git clone git@github.com:Matthew-Redrup/agentic-experiment.git
```
2. Navigate to the project directory
```bash
cd agentic-experiment
```
3. Install the dependencies
```bash
poetry install
```
You will need to have a Postgres Database to point the agent at.  
You will need to create a .env file containing the database URL and OPENAI_API_KEY.

```
DATABASE_URL=""
OPENAI_API_KEY=""
```

## Usage
```bash
poetry run start --prompt "Ask the agent questions about the database"
```

### Example
```bash
poetry run start --prompt "Give me a list of all users with a gmail account"
```
## Release Notes
Using torch 2.0.0 not 2.1.0 as poetry add is not able to pull all the metadata and results in missing dependencies. See [Issue](https://github.com/pytorch/pytorch/issues/104259).
ALternatively can use `poetry add torch`, then manually `pip uninstall torch` and then `pip install torch` again.
