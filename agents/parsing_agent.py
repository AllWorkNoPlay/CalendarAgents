"""
Parsing Agent - Handles file parsing and data extraction (Sprint 2)
"""
from typing import List

from core.mcp import MCPMessage

from .base_agent import BaseAgent


class ParsingAgent(BaseAgent):
    """Agent for parsing schedule files - To be implemented in Sprint 2"""

    def __init__(self):
        super().__init__("parsing_agent", "0.1.0")

    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process parsing requests - Placeholder for Sprint 2"""
        return self.create_success_response(message, {
            "status": "not_implemented",
            "message": "Parsing Agent implementation planned for Sprint 2",
            "agent_id": self.agent_id
        })

    def get_capabilities(self) -> List[str]:
        """Return parsing capabilities"""
        return [
            "parse_pdf",
            "parse_excel",
            "parse_image",
            "extract_schedule_data"
        ]
