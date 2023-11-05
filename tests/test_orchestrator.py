# tests/test_orchestrator.py

import pytest
from agentic_edu.modules.orchestrator import Orchestrator
from autogen import ConversableAgent


def test_add_message():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])
    orchestrator.add_message("Hello, world!")
    assert orchestrator.messages[-1] == "Hello, world!"


def test_has_functions():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])
    assert orchestrator.has_functions(agent1) == (agent1._function_map is not None)
