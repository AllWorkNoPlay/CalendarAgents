"""
API dependencies for the Agentic Scheduler
"""
from core.mcp import message_bus
from agents.orchestrator import OrchestratorAgent

# Global orchestrator instance
orchestrator = OrchestratorAgent()

# Register orchestrator with message bus
message_bus.register_agent("orchestrator", orchestrator)


async def get_orchestrator() -> OrchestratorAgent:
    """Dependency to get the orchestrator agent"""
    return orchestrator


async def get_message_bus():
    """Dependency to get the message bus"""
    return message_bus
