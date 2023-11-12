from agentic_edu.types import Chat, ConversationResult
import pytest


def test_chat_instantiation():
    chat = Chat(from_name="Alice", to_name="Bob", message="Hello")
    assert isinstance(chat, Chat)
    assert chat.from_name == "Alice"
    assert chat.to_name == "Bob"
    assert chat.message == "Hello"


def test_conversation_result_instantiation():
    chat = Chat(from_name="Alice", to_name="Bob", message="Hello")
    result = ConversationResult(
        success=True,
        messages=[chat],
        cost=1.0,
        tokens=10,
        last_message_str="Hello",
        error_message="",
    )
    assert isinstance(result, ConversationResult)
    assert result.success == True
    assert result.messages == [chat]
    assert result.cost == 1.0
    assert result.tokens == 10
    assert result.last_message_str == "Hello"
    assert result.error_message == ""


def test_conversation_result_multiple_messages():
    chat1 = Chat(from_name="Alice", to_name="Bob", message="Hello")
    chat2 = Chat(from_name="Bob", to_name="Alice", message="Hi")
    result = ConversationResult(
        success=True,
        messages=[chat1, chat2],
        cost=1.0,
        tokens=10,
        last_message_str="Hi",
        error_message="",
    )
    assert len(result.messages) == 2
