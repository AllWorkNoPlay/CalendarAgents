"""
Unit tests for utility functions
"""
import pytest
from datetime import datetime

from core.utils import (
    validate_file_type,
    validate_file_size,
    parse_datetime_flexible,
    extract_dates_from_text,
    calculate_overlap,
    is_within_school_year,
    clean_filename
)
from config.settings import ALLOWED_FILE_TYPES


class TestFileValidation:
    """Test file validation utilities"""

    def test_validate_file_type(self):
        """Test file type validation"""
        # Valid types
        assert validate_file_type("document.pdf", ALLOWED_FILE_TYPES) is True
        assert validate_file_type("schedule.xlsx", ALLOWED_FILE_TYPES) is True
        assert validate_file_type("image.png", ALLOWED_FILE_TYPES) is True

        # Invalid types
        assert validate_file_type("document.doc", ALLOWED_FILE_TYPES) is False
        assert validate_file_type("file", ALLOWED_FILE_TYPES) is False
        assert validate_file_type("", ALLOWED_FILE_TYPES) is False

    def test_validate_file_size(self):
        """Test file size validation"""
        max_size = 1024 * 1024  # 1MB

        # Valid sizes
        assert validate_file_size(1024, max_size) is True
        assert validate_file_size(max_size, max_size) is True

        # Invalid sizes
        assert validate_file_size(max_size + 1, max_size) is False
        assert validate_file_size(2048 * 1024, max_size) is False


class TestDateTimeUtils:
    """Test datetime utility functions"""

    def test_parse_datetime_flexible(self):
        """Test flexible datetime parsing"""
        # Test various formats
        dt1 = parse_datetime_flexible("2025-09-01 10:00")
        assert dt1 is not None
        assert dt1.year == 2025
        assert dt1.month == 9
        assert dt1.day == 1

        dt2 = parse_datetime_flexible("09/01/2025")
        assert dt2 is not None

        # Test invalid format
        assert parse_datetime_flexible("invalid") is None

    def test_extract_dates_from_text(self):
        """Test date extraction from text"""
        text = "Meeting on 2025-09-01 at 2 PM and another on September 15, 2025"
        dates = extract_dates_from_text(text)

        assert len(dates) >= 1  # Should find at least one date

    def test_calculate_overlap(self):
        """Test event overlap calculation"""
        # Complete overlap
        overlap = calculate_overlap(
            datetime(2025, 9, 1, 10, 0), datetime(2025, 9, 1, 11, 0),  # Event 1
            datetime(2025, 9, 1, 10, 0), datetime(2025, 9, 1, 11, 0)   # Event 2
        )
        assert overlap == 60  # 60 minutes

        # Partial overlap
        overlap = calculate_overlap(
            datetime(2025, 9, 1, 10, 0), datetime(2025, 9, 1, 11, 0),  # Event 1
            datetime(2025, 9, 1, 10, 30), datetime(2025, 9, 1, 11, 30)  # Event 2
        )
        assert overlap == 30  # 30 minutes

        # No overlap
        overlap = calculate_overlap(
            datetime(2025, 9, 1, 10, 0), datetime(2025, 9, 1, 11, 0),  # Event 1
            datetime(2025, 9, 1, 12, 0), datetime(2025, 9, 1, 13, 0)   # Event 2
        )
        assert overlap == 0

    def test_is_within_school_year(self):
        """Test school year validation"""
        # Within school year
        assert is_within_school_year(datetime(2025, 9, 1)) is True
        assert is_within_school_year(datetime(2025, 12, 15)) is True
        assert is_within_school_year(datetime(2026, 6, 30)) is True

        # Outside school year
        assert is_within_school_year(datetime(2025, 8, 31)) is False
        assert is_within_school_year(datetime(2026, 7, 1)) is False

    def test_clean_filename(self):
        """Test filename cleaning"""
        # Normal filename
        assert clean_filename("test.pdf") == "test.pdf"

        # Filename with spaces
        assert clean_filename("my file.pdf") == "my_file.pdf"

        # Filename with dangerous characters
        assert clean_filename("file<>|?.pdf") == "file.pdf"

        # Long filename
        long_name = "a" * 100 + ".pdf"
        cleaned = clean_filename(long_name)
        assert len(cleaned) <= 104  # 100 + .pdf + some buffer
        assert cleaned.endswith(".pdf")
