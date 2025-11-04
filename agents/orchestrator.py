"""
Orchestrator Agent - Coordinates communication between all agents
"""
from datetime import datetime
from typing import Any, Dict, List

from core.mcp import MCPMessage, message_bus
from core.models import APIResponse

from .base_agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that coordinates all other agents"""

    def __init__(self):
        super().__init__("orchestrator", "0.1.0")
        self.registered_agents: Dict[str, BaseAgent] = {}

    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process orchestrator messages"""
        self.increment_message_count()

        try:
            if message.message_type == "health_check":
                return await self._handle_health_check(message)
            elif message.message_type == "register_agent":
                return await self._handle_register_agent(message)
            elif message.message_type == "list_agents":
                return await self._handle_list_agents(message)
            else:
                return self.create_error_response(
                    message,
                    f"Unknown message type: {message.message_type}"
                )
        except Exception as e:
            self.logger.error(
                "Orchestrator error",
                message_id=message.message_id,
                error=str(e)
            )
            return self.create_error_response(message, f"Internal error: {str(e)}")

    async def _handle_health_check(self, message: MCPMessage) -> MCPMessage:
        """Handle health check requests"""
        agent_health = []
        for agent_id in message_bus.agents:
            try:
                health = await message_bus.agents[agent_id].health_check()
                agent_health.append(health)
            except Exception as e:
                agent_health.append({
                    "agent_id": agent_id,
                    "status": "error",
                    "error": str(e)
                })

        return self.create_success_response(message, {
            "orchestrator_status": "healthy",
            "agents": agent_health,
            "total_agents": len(agent_health)
        })

    async def _handle_register_agent(self, message: MCPMessage) -> MCPMessage:
        """Handle agent registration"""
        if not self.validate_message_payload(message, ["agent_id"]):
            return self.create_error_response(message, "Missing agent_id in payload")

        agent_id = message.payload["agent_id"]

        # For now, just acknowledge registration
        # In a real implementation, this would handle agent discovery
        self.registered_agents[agent_id] = datetime.utcnow()

        return self.create_success_response(message, {
            "registered": True,
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        })

    async def _handle_list_agents(self, message: MCPMessage) -> MCPMessage:
        """Handle request to list all agents"""
        agents_info = []
        for agent_id in message_bus.agents:
            try:
                capabilities = message_bus.agents[agent_id].get_capabilities()
                agents_info.append({
                    "agent_id": agent_id,
                    "capabilities": capabilities,
                    "status": "active"
                })
            except Exception as e:
                agents_info.append({
                    "agent_id": agent_id,
                    "status": "error",
                    "error": str(e)
                })

        return self.create_success_response(message, {
            "agents": agents_info,
            "total_count": len(agents_info)
        })

    def get_capabilities(self) -> List[str]:
        """Return orchestrator capabilities"""
        return [
            "health_check",
            "register_agent",
            "list_agents",
            "coordinate_agents",
            "error_handling"
        ]

    async def coordinate_request(self, target_agent: str, request_type: str,
                               payload: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate a request to another agent"""
        message = MCPMessage(
            message_type=request_type,
            sender=self.agent_id,
            recipient=target_agent,
            payload=payload
        )

        response = await message_bus.send_message(message)

        if response.message_type == "error":
            raise Exception(f"Agent {target_agent} error: {response.payload.get('error', 'Unknown error')}")

        return response.payload.get("data", {})
