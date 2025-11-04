"""
Base agent classes for the Agentic Scheduler
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List

from core.mcp import AgentInterface, MCPMessage
from core.models import AgentHealth


class BaseAgent(AgentInterface, ABC):
    """Base class for all agents in the system"""

    def __init__(self, agent_id: str, version: str = "0.1.0"):
        super().__init__(agent_id)
        self.version = version
        self.start_time = datetime.utcnow()

    @abstractmethod
    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process an incoming MCP message"""
        pass

    async def health_check(self) -> Dict[str, Any]:
        """Return agent health status"""
        uptime = datetime.utcnow() - self.start_time

        return AgentHealth(
            agent_id=self.agent_id,
            status="healthy",
            timestamp=datetime.utcnow(),
            version=self.version,
            capabilities=self.get_capabilities(),
            metrics={
                "uptime_seconds": uptime.total_seconds(),
                "messages_processed": getattr(self, "_messages_processed", 0),
            }
        ).dict()

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of supported operations"""
        pass

    def increment_message_count(self):
        """Increment the message processing counter"""
        if not hasattr(self, "_messages_processed"):
            self._messages_processed = 0
        self._messages_processed += 1

    def validate_message_payload(self, message: MCPMessage, required_fields: List[str]) -> bool:
        """Validate that required fields are present in message payload"""
        for field in required_fields:
            if field not in message.payload:
                self.logger.warning(
                    "Missing required field in message",
                    message_id=message.message_id,
                    field=field
                )
                return False
        return True

    def create_success_response(self, request: MCPMessage, data: Dict[str, Any]) -> MCPMessage:
        """Create a successful response message"""
        return self.create_response(request, {
            "status": "success",
            "data": data
        })

    def create_error_response(self, request: MCPMessage, error_message: str) -> MCPMessage:
        """Create an error response message"""
        return self.create_error_response(request, error_message)


class MockAgent(BaseAgent):
    """Mock agent for testing and development"""

    def __init__(self, agent_id: str, responses: Dict[str, Dict[str, Any]] = None):
        super().__init__(agent_id, "0.1.0-mock")
        self.mock_responses = responses or {}

    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process message with mock responses"""
        self.increment_message_count()

        # Check for predefined mock response
        if message.message_type in self.mock_responses:
            response_data = self.mock_responses[message.message_type]
            return self.create_success_response(message, response_data)

        # Default mock response
        return self.create_success_response(message, {
            "mock_response": True,
            "agent_id": self.agent_id,
            "message_type": message.message_type,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_capabilities(self) -> List[str]:
        """Return mock capabilities"""
        return ["mock_processing", "test_responses"]
