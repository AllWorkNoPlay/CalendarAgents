"""
Utility functions for the Agentic Scheduler
"""
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

import structlog
from dateutil import parser as date_parser

logger = structlog.get_logger(__name__)


def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate file extension against allowed types"""
    if not filename or '.' not in filename:
        return False

    extension = filename.split('.')[-1].lower()
    return extension in allowed_types


def get_file_size_mb(file_size_bytes: int) -> float:
    """Convert file size from bytes to MB"""
    return file_size_bytes / (1024 * 1024)


def validate_file_size(file_size_bytes: int, max_size_bytes: int) -> bool:
    """Validate file size against maximum allowed size"""
    return file_size_bytes <= max_size_bytes


def parse_datetime_flexible(date_str: str) -> Optional[datetime]:
    """Parse date/time string with flexible formats"""
    try:
        # Try common formats
        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M",
            "%m/%d/%Y",
            "%B %d, %Y",
            "%B %d, %Y at %H:%M",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # Try dateutil parser as fallback
        return date_parser.parse(date_str)

    except Exception as e:
        logger.warning("Failed to parse datetime", date_str=date_str, error=str(e))
        return None


def extract_dates_from_text(text: str) -> List[datetime]:
    """Extract dates from natural language text"""
    dates = []

    # Common date patterns
    patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
        r'\b\d{4}-\d{1,2}-\d{1,2}\b',   # YYYY-MM-DD
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',  # Mon DD, YYYY
        r'\btomorrow\b',
        r'\btoday\b',
        r'\bnext\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
        r'\bthis\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            parsed_date = parse_datetime_flexible(match)
            if parsed_date:
                dates.append(parsed_date)

    return dates


def calculate_overlap(event1_start: datetime, event1_end: datetime,
                     event2_start: datetime, event2_end: datetime) -> int:
    """Calculate overlap duration in minutes between two events"""
    overlap_start = max(event1_start, event2_start)
    overlap_end = min(event1_end, event2_end)

    if overlap_start < overlap_end:
        overlap_duration = overlap_end - overlap_start
        return int(overlap_duration.total_seconds() / 60)

    return 0


def is_within_school_year(date: datetime) -> bool:
    """Check if date is within the school year (Sept 2025 - June 2026)"""
    school_year_start = datetime(2025, 9, 1)
    school_year_end = datetime(2026, 6, 30)
    return school_year_start <= date <= school_year_end


def generate_rrule(start_date: datetime, pattern: str) -> str:
    """Generate RRULE string for recurring events"""
    if pattern == "weekly":
        return f"FREQ=WEEKLY;BYDAY={start_date.strftime('%a').upper()};INTERVAL=1"
    elif pattern == "biweekly":
        return f"FREQ=WEEKLY;BYDAY={start_date.strftime('%a').upper()};INTERVAL=2"
    else:
        raise ValueError(f"Unsupported recurrence pattern: {pattern}")


def clean_filename(filename: str) -> str:
    """Clean filename for safe storage"""
    # Remove path separators and dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    return filename


def create_temp_file(content: bytes, filename: str, temp_dir: str = "/tmp") -> str:
    """Create a temporary file and return the path"""
    temp_path = Path(temp_dir) / clean_filename(filename)
    temp_path.write_bytes(content)
    return str(temp_path)


def cleanup_temp_file(file_path: str):
    """Safely remove a temporary file"""
    try:
        Path(file_path).unlink(missing_ok=True)
    except Exception as e:
        logger.warning("Failed to cleanup temp file", file_path=file_path, error=str(e))


def format_datetime_for_display(dt: datetime) -> str:
    """Format datetime for user display"""
    return dt.strftime("%B %d, %Y at %I:%M %p")


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def calculate_confidence_score(text: str, keywords: List[str]) -> float:
    """Calculate confidence score based on keyword matches"""
    if not text or not keywords:
        return 0.0

    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
    return min(matches / len(keywords), 1.0)


def validate_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def safe_json_loads(json_str: str) -> Optional[dict]:
    """Safely parse JSON string"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        logger.warning("Failed to parse JSON", json_str=truncate_text(json_str, 200))
        return None
