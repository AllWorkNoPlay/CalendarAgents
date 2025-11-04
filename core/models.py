"""
Data models for the Agentic Scheduler
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of calendar events"""
    CLASS = "class"
    LAB = "lab"
    STUDY = "study"
    MEETING = "meeting"
    EXAM = "exam"
    OTHER = "other"


class CalendarEvent(BaseModel):
    """Calendar event data model"""
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: datetime
    end_time: datetime
    location: Optional[str] = Field(None, max_length=200)
    recurrence_rule: Optional[str] = None  # RRULE format
    course_code: Optional[str] = Field(None, max_length=50)
    course_name: Optional[str] = Field(None, max_length=200)
    event_type: EventType = EventType.OTHER
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # "weekly", "biweekly"
    metadata: Dict[str, str] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "location": self.location,
            "recurrence_rule": self.recurrence_rule,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "event_type": self.event_type.value,
            "is_recurring": self.is_recurring,
            "recurrence_pattern": self.recurrence_pattern,
            "metadata": self.metadata
        }


class FileUpload(BaseModel):
    """File upload request model"""
    filename: str
    content_type: str
    file_size: int
    content: bytes


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str = Field(..., min_length=1, max_length=1000)
    message_type: str = "user"  # "user", "system", "agent"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CommandResult(BaseModel):
    """Result of processing a natural language command"""
    success: bool
    message: str
    affected_events: List[CalendarEvent] = Field(default_factory=list)
    requires_confirmation: bool = False
    confirmation_message: Optional[str] = None


class ConflictInfo(BaseModel):
    """Information about a scheduling conflict"""
    event1: CalendarEvent
    event2: CalendarEvent
    conflict_type: str  # "overlap", "adjacent", "same_time"
    overlap_duration: int  # minutes
    description: str


class ConflictResolution(BaseModel):
    """Conflict resolution option"""
    id: str
    title: str
    description: str
    action: str  # "keep_both", "keep_first", "keep_second", "reschedule"
    parameters: Dict[str, str] = Field(default_factory=dict)


class NLCommand(BaseModel):
    """Parsed natural language command"""
    raw_text: str
    command_type: str  # "add", "remove", "update", "query", "bulk"
    intent: str  # specific action
    entities: Dict[str, str] = Field(default_factory=dict)  # extracted entities
    confidence_score: float = Field(ge=0.0, le=1.0)
    requires_confirmation: bool = False
    affected_events: List[str] = Field(default_factory=list)  # event IDs


class AgentHealth(BaseModel):
    """Agent health status"""
    agent_id: str
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    version: str = "0.1.0"
    capabilities: List[str] = Field(default_factory=list)
    metrics: Dict[str, float] = Field(default_factory=dict)


class APIResponse(BaseModel):
    """Standard API response"""
    success: bool
    message: str
    data: Optional[Dict] = None
    errors: List[str] = Field(default_factory=list)


class ProcessingStatus(BaseModel):
    """Status of file/event processing"""
    status: str  # "pending", "processing", "completed", "failed"
    progress: float = Field(ge=0.0, le=100.0)
    message: str
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[Dict] = None
