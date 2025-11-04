"""
Calendar Agent - Manages Google Calendar integration
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json

import structlog
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core.mcp import MCPMessage
from core.models import CalendarEvent
from core.utils import is_within_school_year
from config.settings import settings

from .base_agent import BaseAgent

logger = structlog.get_logger(__name__)


class CalendarAgent(BaseAgent):
    """Agent for Google Calendar operations"""

    def __init__(self):
        super().__init__("calendar_agent", "0.2.0")
        self.service = None
        self.calendar_id = settings.google_calendar_id

    async def initialize_calendar_service(self):
        """Initialize Google Calendar API service"""
        if self.service is not None:
            return

        try:
            # For Sprint 2, we'll use API key authentication
            # In production, you'd use service account or OAuth
            if not settings.google_calendar_api_key:
                raise ValueError("GOOGLE_CALENDAR_API_KEY not configured")

            # Create credentials using API key
            # Note: This is a simplified approach. In production, you'd use proper OAuth2
            creds = None  # We'll use API key directly in requests

            # Build the service
            self.service = build('calendar', 'v3', developerKey=settings.google_calendar_api_key)

            logger.info("Google Calendar service initialized")

        except Exception as e:
            logger.error("Failed to initialize Google Calendar service", error=str(e))
            raise

    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process calendar requests"""
        self.increment_message_count()

        try:
            await self.initialize_calendar_service()

            if message.message_type == "create_events":
                return await self._handle_create_events(message)
            elif message.message_type == "list_events":
                return await self._handle_list_events(message)
            elif message.message_type == "delete_events":
                return await self._handle_delete_events(message)
            else:
                return self.create_error_response(
                    message,
                    f"Unknown message type: {message.message_type}"
                )

        except Exception as e:
            logger.error("Calendar agent error", error=str(e), message_id=message.message_id)
            return self.create_error_response(message, f"Calendar operation failed: {str(e)}")

    async def _handle_create_events(self, message: MCPMessage) -> MCPMessage:
        """Create calendar events"""
        if not self.validate_message_payload(message, ["events"]):
            return self.create_error_response(message, "Missing events in payload")

        events_data = message.payload["events"]
        created_events = []

        try:
            for event_data in events_data:
                # Convert dict to CalendarEvent if needed
                if isinstance(event_data, dict):
                    event = CalendarEvent(**event_data)
                else:
                    event = event_data

                # Validate school year constraint
                if not is_within_school_year(event.start_time):
                    logger.warning(
                        "Event outside school year, skipping",
                        title=event.title,
                        start=event.start_time
                    )
                    continue

                # Create the event
                created_event = await self._create_single_event(event)
                if created_event:
                    created_events.append(created_event)

            return self.create_success_response(message, {
                "events_created": len(created_events),
                "events": created_events
            })

        except Exception as e:
            logger.error("Failed to create events", error=str(e))
            return self.create_error_response(message, f"Event creation failed: {str(e)}")

    async def _handle_list_events(self, message: MCPMessage) -> MCPMessage:
        """List calendar events"""
        try:
            # Default to next 30 days if no time range specified
            time_min = message.payload.get("time_min", datetime.utcnow().isoformat() + 'Z')
            time_max = message.payload.get("time_max")

            events_result = await self._list_events(time_min=time_min, time_max=time_max)

            return self.create_success_response(message, {
                "events": events_result
            })

        except Exception as e:
            logger.error("Failed to list events", error=str(e))
            return self.create_error_response(message, f"Event listing failed: {str(e)}")

    async def _handle_delete_events(self, message: MCPMessage) -> MCPMessage:
        """Delete calendar events"""
        if not self.validate_message_payload(message, ["event_ids"]):
            return self.create_error_response(message, "Missing event_ids in payload")

        event_ids = message.payload["event_ids"]
        deleted_count = 0

        try:
            for event_id in event_ids:
                success = await self._delete_single_event(event_id)
                if success:
                    deleted_count += 1

            return self.create_success_response(message, {
                "events_deleted": deleted_count,
                "total_requested": len(event_ids)
            })

        except Exception as e:
            logger.error("Failed to delete events", error=str(e))
            return self.create_error_response(message, f"Event deletion failed: {str(e)}")

    async def _create_single_event(self, event: CalendarEvent) -> Optional[Dict[str, Any]]:
        """Create a single calendar event"""
        try:
            # Convert CalendarEvent to Google Calendar format
            google_event = {
                'summary': event.title,
                'description': event.description or '',
                'start': {
                    'dateTime': event.start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': event.end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'location': event.location or '',
            }

            # Add recurrence if specified
            if event.is_recurring and event.recurrence_rule:
                google_event['recurrence'] = [f"RRULE:{event.recurrence_rule}"]

            # For Sprint 2, we'll simulate the API call since we don't have full Google API setup
            # In production, this would be:
            # created_event = self.service.events().insert(
            #     calendarId=self.calendar_id,
            #     body=google_event
            # ).execute()

            # Mock successful creation
            mock_event = {
                'id': f'mock_event_{datetime.utcnow().timestamp()}',
                'summary': event.title,
                'start': google_event['start'],
                'end': google_event['end'],
                'location': event.location,
                'status': 'confirmed',
                'created': datetime.utcnow().isoformat() + 'Z'
            }

            logger.info("Event created successfully", title=event.title, event_id=mock_event['id'])
            return mock_event

        except Exception as e:
            logger.error("Failed to create event", title=event.title, error=str(e))
            return None

    async def _list_events(self, time_min: str, time_max: Optional[str] = None) -> List[Dict[str, Any]]:
        """List calendar events"""
        try:
            # For Sprint 2, return mock events
            # In production, this would be:
            # events_result = self.service.events().list(
            #     calendarId=self.calendar_id,
            #     timeMin=time_min,
            #     timeMax=time_max,
            #     singleEvents=True,
            #     orderBy='startTime'
            # ).execute()

            # Mock events for demonstration
            mock_events = [
                {
                    'id': 'mock_event_1',
                    'summary': 'Mock Class 1',
                    'start': {'dateTime': '2025-09-01T09:00:00Z'},
                    'end': {'dateTime': '2025-09-01T10:30:00Z'},
                    'location': 'Room 101'
                },
                {
                    'id': 'mock_event_2',
                    'summary': 'Mock Class 2',
                    'start': {'dateTime': '2025-09-01T14:00:00Z'},
                    'end': {'dateTime': '2025-09-01T15:30:00Z'},
                    'location': 'Room 202'
                }
            ]

            logger.info("Events listed successfully", count=len(mock_events))
            return mock_events

        except Exception as e:
            logger.error("Failed to list events", error=str(e))
            return []

    async def _delete_single_event(self, event_id: str) -> bool:
        """Delete a single calendar event"""
        try:
            # For Sprint 2, simulate successful deletion
            # In production, this would be:
            # self.service.events().delete(
            #     calendarId=self.calendar_id,
            #     eventId=event_id
            # ).execute()

            logger.info("Event deleted successfully", event_id=event_id)
            return True

        except Exception as e:
            logger.error("Failed to delete event", event_id=event_id, error=str(e))
            return False

    async def create_event_batch(self, events: List[CalendarEvent]) -> Dict[str, Any]:
        """Create multiple events in batch"""
        results = {
            "successful": [],
            "failed": [],
            "total": len(events)
        }

        for event in events:
            created = await self._create_single_event(event)
            if created:
                results["successful"].append(created)
            else:
                results["failed"].append({
                    "title": event.title,
                    "error": "Creation failed"
                })

        results["success_count"] = len(results["successful"])
        results["failure_count"] = len(results["failed"])

        return results

    def get_capabilities(self) -> List[str]:
        """Return calendar capabilities"""
        return [
            "create_events",
            "update_events",
            "delete_events",
            "list_events",
            "batch_operations",
            "validate_school_year"
        ]
