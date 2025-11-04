"""
API dependencies for the Agentic Scheduler
"""
from core.mcp import message_bus
from agents.orchestrator import OrchestratorAgent
from agents.parsing_agent import ParsingAgent
from agents.calendar_agent import CalendarAgent

# Global agent instances
orchestrator = OrchestratorAgent()
parsing_agent = ParsingAgent()
calendar_agent = CalendarAgent()

# Register agents with message bus
message_bus.register_agent("orchestrator", orchestrator)
message_bus.register_agent("parsing_agent", parsing_agent)
message_bus.register_agent("calendar_agent", calendar_agent)


async def get_orchestrator() -> OrchestratorAgent:
    """Dependency to get the orchestrator agent"""
    return orchestrator


async def get_parsing_agent() -> ParsingAgent:
    """Dependency to get the parsing agent"""
    return parsing_agent


async def get_calendar_agent() -> CalendarAgent:
    """Dependency to get the calendar agent"""
    return calendar_agent


async def get_message_bus():
    """Dependency to get the message bus"""
    return message_bus
