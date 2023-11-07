import pytest
from agentic_edu.modules import orchestrator
from agentic_edu.agents.agents import (
    is_termination_msg,
    build_sr_data_analyst_agent,
    build_team_orchestrator,
    user_proxy,
    data_engineer,
    sr_data_analyst,
    product_manager,
    text_report_analyst,
    json_report_analyst,
    yaml_report_analyst,
)
from agentic_edu.modules.db import PostgresManager
from autogen import AssistantAgent, UserProxyAgent


def test_is_termination_msg():
    assert is_termination_msg({"content": "APPROVED"}) == True
    assert is_termination_msg({"content": "CONTINUE"}) == False
    assert is_termination_msg({"content": ""}) == False
    assert is_termination_msg({"other_key": "APPROVED"}) == False
    assert is_termination_msg({}) == False


def test_agent_creation():
    assert isinstance(user_proxy, UserProxyAgent)
    assert isinstance(data_engineer, AssistantAgent)
    assert isinstance(sr_data_analyst, AssistantAgent)
    assert isinstance(product_manager, AssistantAgent)
    assert isinstance(text_report_analyst, AssistantAgent)
    assert isinstance(json_report_analyst, AssistantAgent)
    assert isinstance(yaml_report_analyst, AssistantAgent)


def test_build_sr_data_analyst_agent():
    db = PostgresManager()
    agent = build_sr_data_analyst_agent(db)

    assert isinstance(agent, AssistantAgent)
    assert agent.name == "Sr_Data_Analyst"


def test_build_sr_data_analyst_agent_invalid_db():
    with pytest.raises(TypeError):
        build_sr_data_analyst_agent("invalid_db")


def test_build_team_orchestrator():
    db = PostgresManager()
    team = "data_eng"
    team_orchestrator = build_team_orchestrator(team, db)

    assert isinstance(team_orchestrator, orchestrator.Orchestrator)
    assert (
        team_orchestrator.name
        == "Postgres Data Analytics Multi-Agent ::: Data Engineering Team"
    )
    assert len(team_orchestrator.agents) == 4

    data_viz_orchestrator = build_team_orchestrator("data_viz", db)
    assert (
        data_viz_orchestrator.name
        == "Postgtrd Data Analytics Multi-Agent ::: Data Viz Team"
    )
    assert len(data_viz_orchestrator.agents) == 4


def test_build_team_orchestrator_invalid_team():
    db = PostgresManager()
    with pytest.raises(ValueError):
        build_team_orchestrator("invalid_team", db)
