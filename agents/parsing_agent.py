"""
Parsing Agent - Handles file parsing and data extraction
"""
import os
import tempfile
from datetime import datetime
from typing import List, Dict, Any
import json

import structlog
from PIL import Image
import pytesseract
import PyPDF2
import openpyxl

from core.mcp import MCPMessage
from core.models import CalendarEvent, ProcessingStatus
from core.ai_client import ai_client
from core.utils import (
    validate_file_type,
    validate_file_size,
    clean_filename,
    create_temp_file,
    cleanup_temp_file
)
from config.settings import settings, ALLOWED_FILE_TYPES

from .base_agent import BaseAgent

logger = structlog.get_logger(__name__)


class ParsingAgent(BaseAgent):
    """Agent for parsing schedule files (PDF, Excel, Images)"""

    def __init__(self):
        super().__init__("parsing_agent", "0.2.0")

    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process parsing requests"""
        self.increment_message_count()

        try:
            if not self.validate_message_payload(message, ["file_data", "filename"]):
                return self.create_error_response(message, "Missing required fields: file_data, filename")

            file_data = message.payload["file_data"]
            filename = message.payload["filename"]

            # Validate file
            if not isinstance(file_data, bytes):
                return self.create_error_response(message, "file_data must be bytes")

            result = await self.parse_schedule_file(file_data, filename)

            return self.create_success_response(message, result)

        except Exception as e:
            logger.error("Parsing agent error", error=str(e), message_id=message.message_id)
            return self.create_error_response(message, f"Parsing failed: {str(e)}")

    async def parse_schedule_file(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Parse schedule file and extract events"""
        try:
            # Validate file type and size
            file_ext = filename.split('.')[-1].lower() if '.' in filename else ''

            if file_ext not in ALLOWED_FILE_TYPES:
                raise ValueError(f"Unsupported file type: {file_ext}. Allowed: {ALLOWED_FILE_TYPES}")

            if len(file_data) > settings.max_file_size:
                raise ValueError(f"File too large: {len(file_data)} bytes. Max: {settings.max_file_size} bytes")

            # Parse based on file type
            if file_ext in ['pdf']:
                events = await self._parse_pdf(file_data, filename)
            elif file_ext in ['xlsx', 'xls']:
                events = await self._parse_excel(file_data, filename)
            elif file_ext in ['png', 'jpg', 'jpeg', 'gif']:
                events = await self._parse_image(file_data, filename)
            else:
                raise ValueError(f"No parser available for file type: {file_ext}")

            return {
                "status": "success",
                "filename": filename,
                "file_size": len(file_data),
                "events_found": len(events),
                "events": [event.to_dict() for event in events],
                "parsed_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error("File parsing failed", filename=filename, error=str(e))
            raise

    async def _parse_pdf(self, file_data: bytes, filename: str) -> List[CalendarEvent]:
        """Parse PDF file and extract schedule events"""
        events = []

        try:
            # Create temporary file
            temp_path = create_temp_file(file_data, filename)

            # Extract text from PDF
            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""

                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"

            # Clean up temp file
            cleanup_temp_file(temp_path)

            # Parse text to extract events (simplified parsing)
            events = self._extract_events_from_text(text_content, "pdf")

        except Exception as e:
            cleanup_temp_file(temp_path)
            logger.error("PDF parsing failed", filename=filename, error=str(e))
            raise

        return events

    async def _parse_excel(self, file_data: bytes, filename: str) -> List[CalendarEvent]:
        """Parse Excel file and extract schedule events"""
        events = []

        try:
            # Create temporary file
            temp_path = create_temp_file(file_data, filename)

            # Load workbook
            workbook = openpyxl.load_workbook(temp_path, data_only=True)
            sheet = workbook.active

            # Extract data from rows (assuming first row is headers)
            rows = list(sheet.iter_rows(values_only=True))
            if len(rows) < 2:
                raise ValueError("Excel file must have at least a header row and one data row")

            # Parse events from rows
            for row in rows[1:]:  # Skip header
                if row[0]:  # If first column has data
                    event = self._parse_excel_row(row)
                    if event:
                        events.append(event)

            # Clean up temp file
            cleanup_temp_file(temp_path)

        except Exception as e:
            cleanup_temp_file(temp_path)
            logger.error("Excel parsing failed", filename=filename, error=str(e))
            raise

        return events

    async def _parse_image(self, file_data: bytes, filename: str) -> List[CalendarEvent]:
        """Parse image file using OCR and AI vision"""
        events = []

        try:
            # Use Azure OpenAI Vision for image processing
            vision_result = await ai_client.parse_schedule_image(file_data, filename)

            if vision_result.get("status") == "mock_processed":
                # For Sprint 2, return mock events
                # In production, this would parse the actual vision result
                mock_events_data = vision_result.get("extracted_events", [])

                for event_data in mock_events_data:
                    event = CalendarEvent(
                        title=event_data.get("title", "Unknown Event"),
                        start_time=datetime.fromisoformat(event_data["start_time"]),
                        end_time=datetime.fromisoformat(event_data["end_time"]),
                        location=event_data.get("location", ""),
                        event_type="class"
                    )
                    events.append(event)
            else:
                # TODO: Parse actual vision API response
                logger.warning("Real vision processing not implemented yet", filename=filename)

        except Exception as e:
            logger.error("Image parsing failed", filename=filename, error=str(e))
            raise

        return events

    def _extract_events_from_text(self, text: str, source: str) -> List[CalendarEvent]:
        """Extract events from text content (simplified implementation)"""
        events = []

        # This is a simplified parser - in production, you'd use more sophisticated NLP
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for patterns like "Class Name - Date Time - Location"
            # This is a very basic parser for demonstration
            if len(line.split('-')) >= 3:
                parts = [part.strip() for part in line.split('-')]
                if len(parts) >= 3:
                    try:
                        event = CalendarEvent(
                            title=parts[0],
                            start_time=datetime.now(),  # Placeholder
                            end_time=datetime.now(),    # Placeholder
                            location=parts[2] if len(parts) > 2 else "",
                            event_type="class"
                        )
                        events.append(event)
                    except Exception as e:
                        logger.warning("Failed to parse event from line", line=line, error=str(e))

        return events

    def _parse_excel_row(self, row: tuple) -> CalendarEvent:
        """Parse a single Excel row into a CalendarEvent"""
        try:
            # Assume format: Title, Date, Start Time, End Time, Location, Type
            if len(row) < 4:
                return None

            title = str(row[0]) if row[0] else "Untitled Event"
            date_str = str(row[1]) if row[1] else None
            start_time_str = str(row[2]) if row[2] else None
            end_time_str = str(row[3]) if row[3] else None
            location = str(row[4]) if len(row) > 4 and row[4] else ""
            event_type = str(row[5]) if len(row) > 5 and row[5] else "class"

            if not all([date_str, start_time_str, end_time_str]):
                return None

            # Combine date and time
            start_datetime = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M")

            return CalendarEvent(
                title=title,
                start_time=start_datetime,
                end_time=end_datetime,
                location=location,
                event_type=event_type
            )

        except Exception as e:
            logger.warning("Failed to parse Excel row", row=row, error=str(e))
            return None

    def get_capabilities(self) -> List[str]:
        """Return parsing capabilities"""
        return [
            "parse_pdf",
            "parse_excel",
            "parse_image",
            "extract_schedule_data",
            "validate_files"
        ]
