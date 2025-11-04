# Agentic Scheduler Requirements Document

## 1. Overview

### 1.1 Project Description
Develop an agentic scheduler system that converts static class schedules from PDF or image files into dynamic Google Calendar events. The system will provide a chatbot-style web interface for uploading schedules and managing calendar changes through natural language commands.

### 1.2 Use Case
As a student, I want to automatically convert my static class schedule (from a PDF or image) into a dynamic digital calendar and be able to manage changes through natural language commands — so I can save time, avoid manual edits, and keep my agenda accurate across all my devices.

## 2. Functional Requirements

### 2.1 Core Functionality

#### 2.1.1 Schedule Upload and Parsing
- **FR-001**: System shall provide a web-based chatbot interface for uploading schedule files
- **FR-002**: System shall accept PDF and image file formats for schedule uploads
- **FR-003**: System shall extract schedule information including course names, dates, times, and locations from uploaded files
- **FR-004**: System shall create corresponding events in a fixed Google Calendar using provided API key

#### 2.1.2 Natural Language Calendar Management
- **FR-005**: System shall accept natural language commands for calendar modifications (e.g., "remove the Calendar items of 27 December")
- **FR-006**: System shall interpret and execute calendar update requests through LLM processing
- **FR-007**: System shall support adding new events via natural language commands

#### 2.1.3 Conflict Detection and Resolution
- **FR-008**: System shall detect scheduling conflicts when new events overlap with existing calendar events
- **FR-009**: System shall present multiple resolution options to the user when conflicts are detected
- **FR-010**: System shall allow users to choose between:
  - Keeping both conflicting events
  - Choosing only one event and removing the other
- **FR-011**: System shall execute the user's chosen conflict resolution

### 2.2 Agent Architecture

#### 2.2.1 Parsing Agent
- **FR-012**: Extract schedule information from PDF and image documents using OpenAI vision and text processing capabilities
- **FR-013**: Convert extracted data into structured event format suitable for calendar integration

#### 2.2.2 Calendar Agent
- **FR-014**: Manage Google Calendar integration using provided API key
- **FR-015**: Create, update, and delete calendar events via Google Calendar API
- **FR-016**: Handle all calendar operations for a single fixed calendar

#### 2.2.3 Change Management Agent
- **FR-017**: Process natural language requests for calendar modifications
- **FR-018**: Interpret user commands and translate them into calendar operations
- **FR-019**: Coordinate with Calendar Agent to execute requested changes

#### 2.2.4 Conflict Evaluation Agent
- **FR-020**: Monitor calendar operations for potential conflicts
- **FR-021**: Detect overlapping events before they are added to the calendar
- **FR-022**: Generate multiple resolution options for conflicts
- **FR-023**: Present options to user through the chatbot interface

#### 2.2.5 Orchestrator
- **FR-024**: Coordinate communication between all agents using MCP (Model Context Protocol)
- **FR-025**: Manage the flow of operations from user input to calendar updates
- **FR-026**: Handle error propagation and recovery across agents

## 3. Technical Requirements

### 3.1 Technology Stack
- **TR-001**: Python as the primary programming language
- **TR-002**: Web framework suitable for creating a chatbot-style interface
- **TR-003**: OpenAI `/chat/completions` API for LLM functionalities
- **TR-004**: Google Calendar API integration
- **TR-005**: MCP (Model Context Protocol) for agent communication

### 3.2 Integration Requirements
- **TR-006**: OpenAI API integration for document interpretation and natural language processing
- **TR-007**: Google Calendar API integration using a fixed API key (no user authentication required)
- **TR-008**: File upload handling for PDF and image formats

### 3.3 User Interface Requirements
- **TR-009**: Basic chatbot-style web interface
- **TR-010**: File upload capability for schedules
- **TR-011**: Text input for natural language commands
- **TR-012**: Display of system responses and conflict resolution options
- **TR-013**: Clear error messages to facilitate debugging

### 3.4 Data Management
- **TR-014**: No local data persistence required beyond Google Calendar
- **TR-015**: API keys stored in `.env` file (ignored by git)
- **TR-016**: Temporary processing of uploaded files without permanent storage

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-001**: Reasonable OpenAI API usage costs (no specific limits)
- **NFR-002**: Response times suitable for interactive chatbot usage

### 4.2 Usability
- **NFR-003**: Intuitive chatbot interface for file uploads and text commands
- **NFR-004**: Clear feedback for all operations and error conditions

### 4.3 Reliability
- **NFR-005**: Clear error messages that facilitate debugging of the proof of concept
- **NFR-006**: Graceful handling of API failures and invalid inputs

### 4.4 Maintainability
- **NFR-007**: Modular agent-based architecture using MCP for communication
- **NFR-008**: Well-documented code and agent responsibilities

## 5. Testing Requirements

### 5.1 Unit Testing
- **TEST-001**: Unit tests for each agent component
- **TEST-002**: Unit tests for utility functions and data processing
- **TEST-003**: Unit tests for API integration functions

### 5.2 Integration Testing
- **TEST-004**: Integration tests for agent communication via MCP
- **TEST-005**: Integration tests for end-to-end schedule upload to calendar creation
- **TEST-006**: Integration tests for natural language command processing
- **TEST-007**: Integration tests for conflict detection and resolution

## 6. Development and Deployment Requirements

### 6.1 Development Environment
- **DEV-001**: Code shall be runnable in VSCode with Python and Git extensions
- **DEV-002**: Project shall use standard Python development practices
- **DEV-003**: API keys shall be configurable via `.env` file (ignored by git)

### 6.2 Deployment
- **DEP-001**: Prototype shall be reproducible by replacing API keys in `.env` file
- **DEP-002**: No complex deployment setup required - standard Python environment
- **DEP-003**: Clear instructions for running and debugging in VSCode

## 7. Deliverables

### 7.1 Technical Documentation
- **DOC-001**: Markdown format documentation
- **DOC-002**: Detailed description of orchestrator and all agents
- **DOC-003**: Clear definition of agent roles and responsibilities
- **DOC-004**: Documentation of agent coordination and communication flows
- **DOC-005**: Architecture overview and data flows

### 7.2 Working Prototype
- **PRO-001**: Functional chatbot web interface
- **PRO-002**: Schedule upload and parsing capability
- **PRO-003**: Google Calendar integration with fixed API key
- **PRO-004**: Natural language calendar management
- **PRO-005**: Conflict detection and resolution system
- **PRO-006**: Comprehensive test suite (unit and integration tests)

## 8. Evaluation Criteria

### 8.1 Functionality (10/30 points)
- Schedule upload and parsing works correctly
- Calendar events are created accurately
- Natural language commands are processed and executed
- Conflict detection and resolution operates as specified

### 8.2 Agentic Design (10/30 points)
- Agents demonstrate autonomy in their respective domains
- Modular design with clear separation of concerns
- Effective collaboration between agents via MCP
- Orchestrator properly coordinates agent interactions

### 8.3 Deliverables (10/30 points)
- Technical documentation is comprehensive and well-structured
- Prototype is functional and reproducible
- Code quality and documentation standards are met
- Test coverage is adequate

## 9. Assumptions and Constraints

### 9.1 Assumptions
- Single user proof-of-concept (fixed Google Calendar)
- OpenAI API access and reasonable usage costs
- Google Calendar API key will be provided
- VSCode with Python and Git extensions available

### 9.2 Constraints
- Only Google Calendar integration required
- No user authentication or multi-user support
- No persistent local data storage
- Proof-of-concept scope (debugging-friendly error handling)
