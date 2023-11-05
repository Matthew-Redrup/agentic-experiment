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


from unittest.mock import patch


def test_basic_chat():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])

    with patch.object(ConversableAgent, "generate_reply", return_value="Hello, world!"):
        responses = orchestrator.basic_chat(agent1, agent2, "Hello, world!")
        assert responses[0] == "basic_chat: Test Agent 1 -> Test Agent 2"
        assert "basic_chat(): replied with: Hello, world!" in responses[1]


def test_memory_chat():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])

    with patch.object(ConversableAgent, "generate_reply", return_value="Hello, world!"):
        responses = orchestrator.memory_chat(agent1, agent2, "Hello, world!")
        assert responses[0] == "memory_chat: Test Agent 1 -> Test Agent 2"


def test_function_chat():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])

    with patch.object(ConversableAgent, "generate_reply", return_value="Hello, world!"):
        responses = orchestrator.function_chat(agent1, agent2, "Hello, world!")
        assert responses[0] == "function_chat(): Test Agent 1 -> Test Agent 2"


def test_properties():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])
    orchestrator.add_message("Hello, world!")
    assert orchestrator.total_agents == 2
    assert orchestrator.last_message_is_dict == False
    assert orchestrator.last_message_is_string == True
    assert orchestrator.last_message_is_func_call == False
    assert orchestrator.last_message_is_content == False
    assert orchestrator.latest_message == "Hello, world!"


def test_sequential_conversation():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])
    with patch.object(ConversableAgent, "generate_reply", return_value="APPROVED"):
        was_successful, messages = orchestrator.sequential_conversation("Hello, world!")
        assert was_successful == True
        assert "Hello, world!" in messages


def test_broadcast_conversation():
    agent1 = ConversableAgent("Test Agent 1")
    agent2 = ConversableAgent("Test Agent 2")
    orchestrator = Orchestrator("Test Orchestrator", [agent1, agent2])
    with patch.object(ConversableAgent, "generate_reply", return_value="APPROVED"):
        was_successful, messages = orchestrator.broadcast_conversation("Hello, world!")
        assert was_successful == True
        assert "Hello, world!" in messages
