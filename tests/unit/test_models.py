"""
Unit tests for data models
"""
import pytest
from datetime import datetime

from core.models import CalendarEvent, EventType


class TestCalendarEvent:
    """Test CalendarEvent model functionality"""

    def test_calendar_event_creation(self):
        """Test basic CalendarEvent creation"""
        event = CalendarEvent(
            title="Test Event",
            start_time=datetime(2025, 9, 1, 10, 0),
            end_time=datetime(2025, 9, 1, 11, 0),
            location="Test Room",
            event_type=EventType.CLASS
        )

        assert event.title == "Test Event"
        assert event.location == "Test Room"
        assert event.event_type == EventType.CLASS
        assert event.is_recurring is False

    def test_calendar_event_to_dict(self):
        """Test CalendarEvent to_dict serialization"""
        event = CalendarEvent(
            id="test-123",
            title="Test Event",
            description="Test description",
            start_time=datetime(2025, 9, 1, 10, 0),
            end_time=datetime(2025, 9, 1, 11, 0),
            location="Test Room",
            course_code="CS101",
            course_name="Computer Science 101",
            event_type=EventType.CLASS,
            is_recurring=True,
            recurrence_pattern="weekly",
            metadata={"priority": "high"}
        )

        event_dict = event.to_dict()

        assert event_dict["id"] == "test-123"
        assert event_dict["title"] == "Test Event"
        assert event_dict["description"] == "Test description"
        assert event_dict["location"] == "Test Room"
        assert event_dict["course_code"] == "CS101"
        assert event_dict["course_name"] == "Computer Science 101"
        assert event_dict["event_type"] == "class"
        assert event_dict["is_recurring"] is True
        assert event_dict["recurrence_pattern"] == "weekly"
        assert event_dict["metadata"]["priority"] == "high"

        # Check datetime serialization
        assert "start_time" in event_dict
        assert "end_time" in event_dict
        assert isinstance(event_dict["start_time"], str)
        assert isinstance(event_dict["end_time"], str)

    def test_calendar_event_validation(self):
        """Test CalendarEvent validation"""
        # Valid event
        event = CalendarEvent(
            title="Valid Event",
            start_time=datetime(2025, 9, 1, 10, 0),
            end_time=datetime(2025, 9, 1, 11, 0)
        )
        assert event.title == "Valid Event"

        # Test required fields
        with pytest.raises(ValueError):
            CalendarEvent(
                # missing title
                start_time=datetime(2025, 9, 1, 10, 0),
                end_time=datetime(2025, 9, 1, 11, 0)
            )

    def test_event_type_enum(self):
        """Test EventType enum values"""
        assert EventType.CLASS.value == "class"
        assert EventType.LAB.value == "lab"
        assert EventType.STUDY.value == "study"
        assert EventType.MEETING.value == "meeting"
        assert EventType.EXAM.value == "exam"
        assert EventType.OTHER.value == "other"

        # Test default value
        event = CalendarEvent(
            title="Test",
            start_time=datetime(2025, 9, 1, 10, 0),
            end_time=datetime(2025, 9, 1, 11, 0)
        )
        assert event.event_type == EventType.OTHER
