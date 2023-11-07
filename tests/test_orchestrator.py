import unittest
from unittest.mock import MagicMock, patch, mock_open
from agentic_edu.modules.orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.mock_agent = MagicMock()
        self.mock_instruments = MagicMock()
        self.orchestrator = Orchestrator(
            "test", [self.mock_agent, self.mock_agent], self.mock_instruments
        )

    def test_init(self):
        self.assertEqual(self.orchestrator.name, "test")
        self.assertEqual(self.orchestrator.agents, [self.mock_agent, self.mock_agent])
        self.assertEqual(self.orchestrator.instruments, self.mock_instruments)
        self.assertEqual(self.orchestrator.messages, [])
        self.assertEqual(self.orchestrator.chats, [])

    def test_send_message(self):
        self.orchestrator.send_message(self.mock_agent, self.mock_agent, "Hello")
        self.assertEqual(len(self.orchestrator.chats), 1)
        self.assertEqual(self.orchestrator.chats[0].message, "Hello")

    def test_add_message(self):
        self.orchestrator.add_message("Hello")
        self.assertEqual(len(self.orchestrator.messages), 1)
        self.assertEqual(self.orchestrator.messages[0], "Hello")

    def test_get_message_as_str(self):
        self.orchestrator.add_message("Hello")
        self.orchestrator.add_message("World")
        self.assertEqual(self.orchestrator.get_message_as_str(), "HelloWorld")

    def test_get_cost_and_tokens(self):
        self.orchestrator.add_message("Hello")
        cost, tokens = self.orchestrator.get_cost_and_tokens()
        self.assertTrue(isinstance(cost, float))
        self.assertTrue(isinstance(tokens, int))

    def test_has_functions(self):
        pass

    def test_basic_chat(self):
        self.orchestrator.basic_chat(self.mock_agent, self.mock_agent, "Hello")
        self.assertEqual(len(self.orchestrator.chats), 1)
        self.assertEqual(self.orchestrator.chats[0].message, "Hello")

    def test_memory_chat(self):
        self.orchestrator.memory_chat(self.mock_agent, self.mock_agent, "Hello")
        self.assertEqual(len(self.orchestrator.chats), 2)

    def test_self_function_chat(self):
        pass

    @patch("builtins.open", new_callable=mock_open)
    def test_spy_on_agents(self, mock_file):
        self.orchestrator.spy_on_agents()
        self.assertTrue(mock_file.called)

    def test_sequential_conversation(self):
        pass

    def test_broadcast_conversation(self):
        self.mock_agent.name = "Mock Agent"
        self.orchestrator.broadcast_conversation("Hello")
        self.assertEqual(len(self.orchestrator.chats), 2)
        self.assertEqual(self.orchestrator.chats[0].message, "Hello")
        self.assertEqual(self.orchestrator.chats[1].message, "Hello")

    def test_round_robin_conversation(self):
        pass


if __name__ == "__main__":
    unittest.main()
