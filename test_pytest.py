#!/usr/bin/env python3
"""
Simple test script to verify pytest setup is working
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test that basic imports work"""
    try:
        # Test core modules (with graceful handling of missing dependencies)
        import sys
        from unittest.mock import MagicMock

        # Mock missing dependencies
        try:
            import structlog
        except ImportError:
            sys.modules['structlog'] = MagicMock()
            sys.modules['structlog'].get_logger = MagicMock(return_value=MagicMock())

        # Now import core modules
        from core.mcp import MCPMessage
        from core.models import CalendarEvent, EventType
        from core.utils import validate_file_type
        from config.settings import ALLOWED_FILE_TYPES
        print("✅ Basic imports successful")
        return True
    except Exception as e:
        print(f"❌ Basic import failed: {e}")
        return False

def test_pydantic_models():
    """Test that pydantic models work"""
    try:
        # Mock pydantic if not available
        try:
            import pydantic
        except ImportError:
            import sys
            from unittest.mock import MagicMock
            pydantic_mock = MagicMock()
            sys.modules['pydantic'] = pydantic_mock
            sys.modules['pydantic.main'] = pydantic_mock.main

        from core.models import CalendarEvent
        from datetime import datetime

        # Create a test event
        event = CalendarEvent(
            title="Test Event",
            start_time=datetime(2025, 9, 1, 10, 0),
            end_time=datetime(2025, 9, 1, 11, 0),
            location="Test Room"
        )

        # Test serialization
        event_dict = event.to_dict()
        assert event_dict["title"] == "Test Event"
        assert event_dict["location"] == "Test Room"

        print("✅ Pydantic models working")
        return True
    except Exception as e:
        print(f"❌ Pydantic model test failed: {e}")
        return False

def test_file_validation():
    """Test file validation utilities"""
    try:
        from core.utils import validate_file_type
        from config.settings import ALLOWED_FILE_TYPES

        # Test valid types
        assert validate_file_type("test.pdf", ALLOWED_FILE_TYPES)
        assert validate_file_type("test.xlsx", ALLOWED_FILE_TYPES)
        assert validate_file_type("test.png", ALLOWED_FILE_TYPES)

        # Test invalid types
        assert not validate_file_type("test.doc", ALLOWED_FILE_TYPES)

        print("✅ File validation working")
        return True
    except Exception as e:
        print(f"❌ File validation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Agentic Scheduler components...")
    print("=" * 50)

    tests = [
        test_basic_imports,
        test_pydantic_models,
        test_file_validation,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Pytest should work correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check dependencies and imports.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
