"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up minimal environment for testing
os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('DEBUG', 'true')
os.environ.setdefault('OPENAI_API_KEY', 'test-key')
os.environ.setdefault('GOOGLE_CALENDAR_API_KEY', 'test-key')
os.environ.setdefault('GOOGLE_CALENDAR_ID', 'test-calendar-id')

# Mock optional dependencies that might not be available during testing
try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    # Mock structlog if not available
    structlog_mock = MagicMock()
    structlog_mock.get_logger.return_value = MagicMock()
    sys.modules['structlog'] = structlog_mock
    STRUCTLOG_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    # Mock pytesseract if not available
    sys.modules['pytesseract'] = MagicMock()
    PYTESSERACT_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    # Mock PIL if not available
    pil_mock = MagicMock()
    sys.modules['PIL'] = pil_mock
    sys.modules['PIL.Image'] = pil_mock.Image
    PIL_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    # Mock PyPDF2 if not available
    sys.modules['PyPDF2'] = MagicMock()
    PYPDF2_AVAILABLE = False

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    # Mock openpyxl if not available
    sys.modules['openpyxl'] = MagicMock()
    OPENPYXL_AVAILABLE = False

try:
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    # Mock google API if not available
    google_mock = MagicMock()
    sys.modules['googleapiclient'] = google_mock
    sys.modules['googleapiclient.discovery'] = google_mock.discovery
    sys.modules['google.oauth2.credentials'] = MagicMock()
    sys.modules['googleapiclient.errors'] = MagicMock()
    GOOGLE_API_AVAILABLE = False

try:
    from openai import AsyncOpenAI, AsyncAzureOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    # Mock openai if not available
    openai_mock = MagicMock()
    sys.modules['openai'] = openai_mock
    OPENAI_AVAILABLE = False


@pytest.fixture(scope="session")
def test_app():
    """Create test app instance"""
    try:
        from main import app
        return app
    except ImportError as e:
        pytest.skip(f"App dependencies not available: {e}")


@pytest.fixture
def test_client(test_app):
    """Create test client"""
    try:
        from fastapi.testclient import TestClient
        return TestClient(test_app)
    except ImportError:
        pytest.skip("FastAPI TestClient not available")


@pytest.fixture
def sample_file_content():
    """Sample file content for testing"""
    return b"Mathematics 101 - Monday 9:00 AM - Room 101\nPhysics Lab - Tuesday 2:00 PM - Lab 205"


@pytest.fixture
def sample_excel_data():
    """Sample Excel-like data for testing"""
    return [
        ["Title", "Date", "Start Time", "End Time", "Location", "Type"],
        ["Math Class", "2025-09-01", "09:00", "10:30", "Room 101", "class"],
        ["Physics Lab", "2025-09-02", "14:00", "16:00", "Lab 205", "lab"]
    ]
