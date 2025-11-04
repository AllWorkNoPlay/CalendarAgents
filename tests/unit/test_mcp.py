"""
Unit tests for MCP (Model Context Protocol) implementation
"""
import pytest
from datetime import datetime

from core.mcp import MCPMessage, MCPException


class TestMCPMessage:
    """Test MCP Message functionality"""

    def test_message_creation(self):
        """Test basic message creation"""
        message = MCPMessage(
            message_type="test",
            sender="test_agent",
            recipient="orchestrator",
            payload={"key": "value"}
        )

        assert message.message_type == "test"
        assert message.sender == "test_agent"
        assert message.recipient == "orchestrator"
        assert message.payload == {"key": "value"}
        assert message.protocol_version == "1.0"
        assert message.message_id is not None
        assert message.conversation_id is not None

    def test_message_serialization(self):
        """Test message JSON serialization"""
        message = MCPMessage(
            message_type="test",
            sender="test_agent",
            recipient="orchestrator",
            payload={"key": "value"}
        )

        # Test to dict
        msg_dict = message.to_dict()
        assert isinstance(msg_dict, dict)
        assert msg_dict["message_type"] == "test"

        # Test to JSON
        msg_json = message.to_json()
        assert isinstance(msg_json, str)

        # Test from JSON
        message2 = MCPMessage.from_json(msg_json)
        assert message2.message_type == message.message_type
        assert message2.sender == message.sender
        assert message2.payload == message.payload

    def test_message_with_conversation(self):
        """Test message with conversation context"""
        conversation_id = "test-conversation-123"
        correlation_id = "test-correlation-456"

        message = MCPMessage(
            message_type="request",
            sender="agent1",
            recipient="agent2",
            payload={"action": "test"},
            conversation_id=conversation_id,
            correlation_id=correlation_id
        )

        assert message.conversation_id == conversation_id
        assert message.correlation_id == correlation_id

    def test_message_timestamps(self):
        """Test message timestamp handling"""
        before = datetime.utcnow()
        message = MCPMessage(
            message_type="test",
            sender="test",
            recipient="test",
            payload={}
        )
        after = datetime.utcnow()

        # Parse the timestamp
        timestamp = datetime.fromisoformat(message.timestamp.replace('Z', '+00:00'))

        assert before <= timestamp <= after


class TestMCPException:
    """Test MCP exception handling"""

    def test_basic_exception(self):
        """Test basic MCP exception"""
        exc = MCPException("Test error")
        assert str(exc) == "Test error"
        assert exc.message_id is None

    def test_exception_with_message_id(self):
        """Test exception with message ID"""
        message_id = "test-msg-123"
        exc = MCPException("Test error", message_id)
        assert str(exc) == "Test error"
        assert exc.message_id == message_id


class TestMessageBus:
    """Test message bus functionality"""

    def test_message_bus_creation(self):
        """Test message bus initialization"""
        from core.mcp import MessageBus

        bus = MessageBus()
        assert hasattr(bus, 'agents')
        assert hasattr(bus, 'message_queue')
        assert len(bus.agents) == 0

    def test_agent_registration(self):
        """Test agent registration"""
        from core.mcp import MessageBus, AgentInterface

        class MockAgent(AgentInterface):
            def __init__(self):
                super().__init__("mock_agent")

            async def process_message(self, message):
                return self.create_success_response(message, {"result": "mock"})

            def get_capabilities(self):
                return ["mock"]

        bus = MessageBus()
        agent = MockAgent()

        bus.register_agent("mock_agent", agent)
        assert "mock_agent" in bus.agents
        assert bus.agents["mock_agent"] == agent

    def test_agent_unregistration(self):
        """Test agent unregistration"""
        from core.mcp import MessageBus, AgentInterface

        class MockAgent(AgentInterface):
            def __init__(self):
                super().__init__("mock_agent")

            async def process_message(self, message):
                return self.create_success_response(message, {"result": "mock"})

            def get_capabilities(self):
                return ["mock"]

        bus = MessageBus()
        agent = MockAgent()

        bus.register_agent("mock_agent", agent)
        assert "mock_agent" in bus.agents

        bus.unregister_agent("mock_agent")
        assert "mock_agent" not in bus.agents

    def test_message_routing(self):
        """Test message routing to agents"""
        import asyncio
        from core.mcp import MessageBus, AgentInterface

        class MockAgent(AgentInterface):
            def __init__(self):
                super().__init__("mock_agent")

            async def process_message(self, message):
                return self.create_success_response(message, {"result": "processed"})

            def get_capabilities(self):
                return ["mock"]

        async def test_routing():
            bus = MessageBus()
            agent = MockAgent()
            bus.register_agent("mock_agent", agent)

            message = MCPMessage(
                message_type="test",
                sender="test_sender",
                recipient="mock_agent",
                payload={"action": "test"}
            )

            response = await bus.send_message(message)
            assert response.message_type == "response"
            assert response.payload["data"]["result"] == "processed"

        asyncio.run(test_routing())

    def test_unknown_agent_error(self):
        """Test error handling for unknown agents"""
        import asyncio
        from core.mcp import MessageBus

        async def test_unknown_agent():
            bus = MessageBus()

            message = MCPMessage(
                message_type="test",
                sender="test_sender",
                recipient="unknown_agent",
                payload={"action": "test"}
            )

            with pytest.raises(MCPException) as exc_info:
                await bus.send_message(message)

            assert "unknown_agent" in str(exc_info.value)

        asyncio.run(test_unknown_agent())
