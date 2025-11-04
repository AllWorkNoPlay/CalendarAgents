"""
Model Context Protocol (MCP) implementation for agent communication
"""
import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)


class MCPMessage:
    """MCP Message structure"""

    def __init__(
        self,
        message_type: str,
        sender: str,
        recipient: str,
        payload: Dict[str, Any],
        conversation_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ):
        self.protocol_version = "1.0"
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type  # request, response, notification
        self.payload = payload
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.correlation_id = correlation_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "protocol_version": self.protocol_version,
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type,
            "payload": self.payload,
            "conversation_id": self.conversation_id,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPMessage":
        """Create message from dictionary"""
        return cls(
            message_type=data["message_type"],
            sender=data["sender"],
            recipient=data["recipient"],
            payload=data["payload"],
            conversation_id=data.get("conversation_id"),
            correlation_id=data.get("correlation_id"),
            message_id=data.get("message_id"),
        )

    def to_json(self) -> str:
        """Convert message to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "MCPMessage":
        """Create message from JSON string"""
        return cls.from_dict(json.loads(json_str))


class MCPException(Exception):
    """Base exception for MCP-related errors"""

    def __init__(self, message: str, message_id: Optional[str] = None):
        super().__init__(message)
        self.message_id = message_id


class MCPTimeoutError(MCPException):
    """Exception raised when MCP message times out"""
    pass


class MessageBus:
    """Central message bus for MCP communication"""

    def __init__(self):
        self.agents: Dict[str, "AgentInterface"] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.logger = structlog.get_logger(__name__)

    def register_agent(self, agent_id: str, agent: "AgentInterface"):
        """Register an agent with the message bus"""
        self.agents[agent_id] = agent
        self.logger.info("Agent registered", agent_id=agent_id)

    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the message bus"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.logger.info("Agent unregistered", agent_id=agent_id)

    async def send_message(self, message: MCPMessage) -> MCPMessage:
        """Send a message to the appropriate agent"""
        if message.recipient not in self.agents:
            raise MCPException(f"Agent {message.recipient} not found")

        agent = self.agents[message.recipient]

        try:
            self.logger.info(
                "Sending message",
                message_id=message.message_id,
                sender=message.sender,
                recipient=message.recipient,
                message_type=message.message_type
            )

            response = await agent.process_message(message)

            self.logger.info(
                "Message processed successfully",
                message_id=message.message_id,
                response_type=response.message_type
            )

            return response

        except Exception as e:
            error_message = MCPMessage(
                message_type="error",
                sender=message.recipient,
                recipient=message.sender,
                payload={"error": str(e), "error_type": type(e).__name__},
                conversation_id=message.conversation_id,
                correlation_id=message.message_id,
            )
            self.logger.error(
                "Message processing failed",
                message_id=message.message_id,
                error=str(e)
            )
            return error_message


# Global message bus instance
message_bus = MessageBus()


class AgentInterface:
    """Base interface for all agents"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = structlog.get_logger(f"agent.{agent_id}")

    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process an incoming MCP message"""
        raise NotImplementedError("Subclasses must implement process_message")

    async def health_check(self) -> Dict[str, Any]:
        """Return agent health status"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_capabilities(self) -> list:
        """Return list of supported operations"""
        return []

    def create_response(self, request: MCPMessage, payload: Dict[str, Any]) -> MCPMessage:
        """Create a response message"""
        return MCPMessage(
            message_type="response",
            sender=self.agent_id,
            recipient=request.sender,
            payload=payload,
            conversation_id=request.conversation_id,
            correlation_id=request.message_id,
        )

    def create_error_response(self, request: MCPMessage, error: str) -> MCPMessage:
        """Create an error response message"""
        return MCPMessage(
            message_type="error",
            sender=self.agent_id,
            recipient=request.sender,
            payload={"error": error},
            conversation_id=request.conversation_id,
            correlation_id=request.message_id,
        )


async def send_message_to_agent(
    recipient: str,
    message_type: str,
    payload: Dict[str, Any],
    sender: str = "system",
    timeout: int = 30
) -> MCPMessage:
    """Convenience function to send a message to an agent"""
    message = MCPMessage(
        message_type=message_type,
        sender=sender,
        recipient=recipient,
        payload=payload,
    )

    try:
        return await asyncio.wait_for(
            message_bus.send_message(message),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise MCPTimeoutError(f"Message to {recipient} timed out", message.message_id)
