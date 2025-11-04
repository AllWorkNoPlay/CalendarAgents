# Natural Language Command Use Cases

## Overview
This document defines the natural language command use cases for the agentic scheduler system. Commands should be intuitive and conversational, allowing users to manage their calendar through natural language interactions.

## Use Case Categories

### 1. Event Removal Commands

**UC-NL-001: Remove Events by Date**
- Sample Commands:
  - "Remove all calendar items on December 27th"
  - "Delete everything scheduled for next Friday"
  - "Cancel my appointments on January 15, 2026"
  - "Clear my schedule for tomorrow"

**UC-NL-002: Remove Events by Subject/Course**
- Sample Commands:
  - "Remove all Math 101 classes"
  - "Delete Physics lectures from my calendar"
  - "Cancel all Computer Science labs"
  - "Remove the Biology class scheduled for this week"

**UC-NL-003: Remove Events by Time Period**
- Sample Commands:
  - "Remove all events for this week"
  - "Delete everything scheduled in December"
  - "Cancel my appointments for the next two weeks"
  - "Clear my schedule from Monday to Friday next week"

### 2. Event Addition Commands

**UC-NL-004: Add Single Events**
- Sample Commands:
  - "Add a study session for Math 101 on Wednesday at 3 PM"
  - "Schedule a meeting with my professor on Friday at 2 PM"
  - "Add a doctor's appointment for next Tuesday at 10 AM"
  - "Create an event for group project work on Thursday from 4-6 PM"

**UC-NL-005: Add Recurring Events**
- Sample Commands:
  - "Add weekly Math 101 classes every Monday and Wednesday at 9 AM"
  - "Schedule bi-weekly Physics labs starting next Tuesday at 2 PM"
  - "Create a recurring study group every Friday from 5-7 PM"
  - "Add daily reminders for exam preparation from Monday to Friday at 8 PM"

### 3. Event Modification Commands

**UC-NL-006: Reschedule Events**
- Sample Commands:
  - "Move my Math class from Wednesday to Thursday"
  - "Reschedule the Physics lab to next week"
  - "Change the time of my meeting on Friday to 3 PM"
  - "Move all Monday classes to Tuesday this week"

**UC-NL-007: Update Event Details**
- Sample Commands:
  - "Change the location of tomorrow's class to Room 205"
  - "Update the description for my Biology lab"
  - "Rename the Math study session to 'Calculus Review'"
  - "Add notes to the Computer Science project meeting"

### 4. Query and Information Commands

**UC-NL-008: Check Schedule**
- Sample Commands:
  - "What's on my schedule for today?"
  - "Show me my classes for this week"
  - "When is my next Physics lab?"
  - "What do I have scheduled on Friday?"

**UC-NL-009: Check Conflicts**
- Sample Commands:
  - "Are there any conflicts in my schedule this week?"
  - "Do I have overlapping appointments tomorrow?"
  - "Check if my new study session conflicts with existing events"
  - "Show me any scheduling conflicts for next Monday"

### 5. Bulk Operations Commands

**UC-NL-010: Bulk Modifications**
- Sample Commands:
  - "Move all my morning classes to afternoon"
  - "Cancel all events after 5 PM this week"
  - "Reschedule all Monday classes to Tuesday"
  - "Change the location for all Math classes to Room 101"

**UC-NL-011: Pattern-based Operations**
- Sample Commands:
  - "Remove all recurring events that start with 'Study'"
  - "Cancel all events in the Science building"
  - "Move all 9 AM classes to 10 AM"
  - "Update all Physics events to include 'Bring lab notebook'"

## Command Processing Guidelines

### Natural Language Understanding
- Commands should be flexible and accept various phrasings
- Support for relative dates (today, tomorrow, next week, etc.)
- Time expressions (9 AM, 2 PM, morning, afternoon, etc.)
- Subject/course name recognition
- Location references

### Response Format
- Confirm successful operations
- Show affected events when multiple items are impacted
- Ask for clarification when commands are ambiguous
- Provide options for conflict resolution when needed

### Error Handling
- Graceful handling of invalid commands
- Suggestions for correcting malformed commands
- Clear feedback when operations cannot be completed

## Implementation Notes

### LLM Integration
- Use OpenAI's chat completions for command interpretation
- Provide context about existing calendar events
- Maintain conversation history for follow-up commands

### Command Categories Priority
1. Safety-critical operations (conflict detection)
2. Event modifications (update, reschedule)
3. Event creation (add new events)
4. Event removal (delete operations)
5. Query operations (check schedule)

### Validation Rules
- All dates must fall within school year (Sept 2025 - June 2026)
- Prevent scheduling outside business hours (reasonable limits)
- Validate against existing conflicts
- Confirm bulk operations before execution
