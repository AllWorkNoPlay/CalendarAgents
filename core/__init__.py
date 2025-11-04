"""
Core functionality for the Agentic Scheduler
"""
from .mcp import MCPMessage, message_bus, send_message_to_agent
from .models import (
    CalendarEvent,
    FileUpload,
    ChatMessage,
    CommandResult,
    ConflictInfo,
    ConflictResolution,
    NLCommand,
    AgentHealth,
    APIResponse,
    ProcessingStatus,
    EventType,
)
from .utils import (
    validate_file_type,
    get_file_size_mb,
    validate_file_size,
    parse_datetime_flexible,
    extract_dates_from_text,
    calculate_overlap,
    is_within_school_year,
    generate_rrule,
    clean_filename,
    create_temp_file,
    cleanup_temp_file,
    format_datetime_for_display,
    truncate_text,
    calculate_confidence_score,
    validate_email,
    safe_json_loads,
)
from .ai_client import ai_client, AIClient

__all__ = [
    # MCP
    "MCPMessage",
    "message_bus",
    "send_message_to_agent",
    # Models
    "CalendarEvent",
    "FileUpload",
    "ChatMessage",
    "CommandResult",
    "ConflictInfo",
    "ConflictResolution",
    "NLCommand",
    "AgentHealth",
    "APIResponse",
    "ProcessingStatus",
    "EventType",
    # Utils
    "validate_file_type",
    "get_file_size_mb",
    "validate_file_size",
    "parse_datetime_flexible",
    "extract_dates_from_text",
    "calculate_overlap",
    "is_within_school_year",
    "generate_rrule",
    "clean_filename",
    "create_temp_file",
    "cleanup_temp_file",
    "format_datetime_for_display",
    "truncate_text",
    "calculate_confidence_score",
    "validate_email",
    "safe_json_loads",
    # AI Client
    "ai_client",
    "AIClient",
]
