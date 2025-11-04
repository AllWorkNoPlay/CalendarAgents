"""
AI Client for OpenAI and Azure OpenAI integration
"""
import asyncio
from typing import Dict, Any, Optional, List

import structlog
from openai import AsyncOpenAI, AsyncAzureOpenAI

from .models import NLCommand, ProcessingStatus
from config.settings import settings

logger = structlog.get_logger(__name__)


class AIClient:
    """Unified client for OpenAI and Azure OpenAI operations"""

    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None
        self._initialized = False

    async def initialize(self):
        """Initialize the appropriate AI client based on configuration"""
        if self._initialized:
            return

        try:
            # Check for Azure OpenAI configuration first
            if (settings.azure_openai_api_key and
                settings.azure_openai_endpoint and
                settings.azure_openai_deployment_name):

                logger.info("Initializing Azure OpenAI client")
                self.client = AsyncAzureOpenAI(
                    api_key=settings.azure_openai_api_key,
                    api_version=settings.azure_openai_api_version,
                    azure_endpoint=settings.azure_openai_endpoint,
                )
                self.deployment_name = settings.azure_openai_deployment_name
                self.is_azure = True

            # Fall back to regular OpenAI
            elif settings.openai_api_key:
                logger.info("Initializing OpenAI client")
                self.client = AsyncOpenAI(api_key=settings.openai_api_key)
                self.deployment_name = None
                self.is_azure = False

            else:
                raise ValueError(
                    "No AI configuration found. Please set either:\n"
                    "- OPENAI_API_KEY for OpenAI, or\n"
                    "- AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT_NAME for Azure OpenAI"
                )

            self._initialized = True
            logger.info("AI client initialized successfully", is_azure=self.is_azure)

        except Exception as e:
            logger.error("Failed to initialize AI client", error=str(e))
            raise

    async def parse_schedule_image(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Parse schedule information from an image using vision capabilities

        Args:
            image_data: Raw image bytes
            filename: Original filename for context

        Returns:
            Dict containing parsed schedule data
        """
        await self.initialize()

        # For now, return a mock response since we don't have actual image processing
        # In Sprint 2, this will be implemented with actual vision API calls
        logger.info("Processing schedule image", filename=filename, size=len(image_data))

        # Mock response for Sprint 2 development
        return {
            "status": "mock_processed",
            "filename": filename,
            "events_found": 2,
            "message": "Image processing implemented in Sprint 2",
            "mock_data": True,
            "extracted_events": [
                {
                    "title": "Mock Class 1",
                    "start_time": "2025-09-01T09:00:00",
                    "end_time": "2025-09-01T10:30:00",
                    "location": "Room 101"
                },
                {
                    "title": "Mock Class 2",
                    "start_time": "2025-09-01T14:00:00",
                    "end_time": "2025-09-01T15:30:00",
                    "location": "Room 202"
                }
            ]
        }

    async def interpret_natural_language(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> NLCommand:
        """
        Interpret natural language commands using chat completion

        Args:
            user_message: The user's natural language input
            context: Optional context about current calendar state

        Returns:
            Parsed NLCommand object
        """
        await self.initialize()

        system_prompt = """
        You are an AI assistant that helps users manage their calendar through natural language commands.
        Analyze the user's message and determine what calendar operation they want to perform.

        Supported operations:
        - Add events: "schedule a meeting tomorrow at 3pm"
        - Remove events: "cancel my appointment on friday"
        - Update events: "move my class to 4pm"
        - Query events: "what do I have scheduled today?"
        - Bulk operations: "clear all events this week"

        Return a JSON response with:
        - command_type: "add", "remove", "update", "query", "bulk"
        - intent: specific action description
        - entities: extracted dates, times, subjects, etc.
        - confidence_score: 0.0-1.0
        - requires_confirmation: true/false
        """

        user_context = ""
        if context:
            user_context = f"\nCurrent context: {context}"

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User message: {user_message}{user_context}"}
            ]

            # Use deployment name for Azure, model name for OpenAI
            if self.is_azure:
                response = await self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.1
                )
            else:
                response = await self.client.chat.completions.create(
                    model="gpt-4",  # Default to GPT-4
                    messages=messages,
                    max_tokens=500,
                    temperature=0.1
                )

            result_text = response.choices[0].message.content
            logger.info("AI interpretation completed", input_length=len(user_message))

            # For Sprint 1, return a mock command since full NLP will be in Sprint 3
            return NLCommand(
                raw_text=user_message,
                command_type="mock",
                intent="mock_command",
                confidence_score=0.5,
                requires_confirmation=False,
                entities={"mock": True}
            )

        except Exception as e:
            logger.error("AI interpretation failed", error=str(e), user_message=user_message[:100])
            # Return a safe fallback command
            return NLCommand(
                raw_text=user_message,
                command_type="unknown",
                intent="failed_to_parse",
                confidence_score=0.0,
                requires_confirmation=True,
                entities={"error": str(e)}
            )

    async def health_check(self) -> Dict[str, Any]:
        """Check AI client health"""
        try:
            await self.initialize()
            return {
                "status": "healthy",
                "client_type": "azure_openai" if self.is_azure else "openai",
                "deployment": self.deployment_name if self.is_azure else "gpt-4"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global AI client instance
ai_client = AIClient()
