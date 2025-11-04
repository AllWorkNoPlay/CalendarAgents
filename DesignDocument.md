# Agentic Scheduler System Design Document

## 1. System Overview

### 1.1 Project Description
The Agentic Scheduler is a web-based chatbot system that converts static class schedules from PDF, Excel, and image files into dynamic Google Calendar events. The system provides natural language interfaces for managing calendar modifications while detecting and resolving scheduling conflicts.

### 1.2 Key Features
- **Multi-format Schedule Parsing**: Support for PDF, Excel, and common image formats
- **Intelligent Conflict Detection**: Automated detection and resolution of scheduling conflicts
- **Natural Language Processing**: Conversational interface for calendar management
- **Agentic Architecture**: Modular design using specialized agents communicating via MCP
- **School Year Constraints**: Enforced scheduling within September 2025 - June 2026
- **Recurring Event Support**: Weekly and bi-weekly subject scheduling

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │    Orchestrator │    │   Google        │
│   (Chatbot UI)  │◄──►│     Agent       │◄──►│   Calendar      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Parsing       │    │   Change Mgmt   │    │   Conflict      │
│   Agent         │    │   Agent         │    │   Evaluation    │
│                 │    │                 │    │   Agent         │
│ • PDF/Excel/Image│    │ • NLP Commands  │    │ • Conflict      │
│   Processing    │    │ • Event CRUD    │    │   Detection     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.2 Agent Architecture

#### 2.2.1 Orchestrator Agent
**Responsibilities:**
- Coordinate communication between all agents
- Manage request routing and response aggregation
- Handle error propagation and recovery
- Maintain conversation state

**MCP Communication:**
```json
{
  "message_type": "orchestrator_request",
  "request_id": "uuid",
  "target_agent": "parsing_agent",
  "payload": {...},
  "conversation_context": {...}
}
```

#### 2.2.2 Parsing Agent
**Responsibilities:**
- Extract schedule data from uploaded files (PDF, Excel, Images)
- Convert extracted data to structured event format
- Handle OCR for image-based schedules
- Validate extracted data against school year constraints

**Input/Output:**
- Input: File bytes + metadata (format, filename)
- Output: Structured event list with validation results

#### 2.2.3 Calendar Agent
**Responsibilities:**
- Interface with Google Calendar API
- CRUD operations on calendar events
- Batch event creation/updates/deletion
- Handle API rate limits and errors

**Google Calendar Integration:**
- Uses service account authentication
- Single fixed calendar ID
- Event format standardization

#### 2.2.4 Change Management Agent
**Responsibilities:**
- Parse and interpret natural language commands
- Translate commands to calendar operations
- Handle complex multi-step commands
- Validate command parameters

**NLP Integration:**
- OpenAI Chat Completions API
- Command classification and entity extraction
- Context-aware response generation

#### 2.2.5 Conflict Evaluation Agent
**Responsibilities:**
- Monitor calendar operations for conflicts
- Detect overlapping events before creation
- Generate resolution options
- Present conflict choices to users

**Conflict Detection Logic:**
- Time overlap detection
- Priority-based conflict resolution
- User preference learning

## 3. Data Models and Structures

### 3.1 Event Data Structure
```python
class CalendarEvent:
    id: str
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    recurrence_rule: str  # RRULE format
    course_code: str
    course_name: str
    event_type: str  # "class", "lab", "study", "meeting"
    is_recurring: bool
    recurrence_pattern: str  # "weekly", "biweekly"
    metadata: dict
```

### 3.2 MCP Message Format
```json
{
  "protocol_version": "1.0",
  "message_id": "uuid",
  "timestamp": "ISO8601",
  "sender": "agent_name",
  "recipient": "agent_name",
  "message_type": "request|response|notification",
  "payload": {
    "action": "create_events|update_event|delete_events|parse_schedule|...",
    "data": {...},
    "metadata": {...}
  },
  "conversation_id": "uuid",
  "correlation_id": "uuid"
}
```

### 3.3 Natural Language Command Structure
```python
class NLCommand:
    raw_text: str
    command_type: str  # "add", "remove", "update", "query", "bulk"
    intent: str  # specific action
    entities: dict  # extracted entities (dates, times, subjects, etc.)
    confidence_score: float
    requires_confirmation: bool
    affected_events: list
```

## 4. API Design

### 4.1 Web Interface Endpoints
```
POST /api/upload-schedule
- Upload and process schedule files
- Returns: processing status and extracted events

POST /api/chat
- Process natural language commands
- Returns: command interpretation and execution results

GET /api/calendar/events
- Retrieve calendar events with filtering
- Query params: date_range, subject, location

GET /api/conflicts
- Check for scheduling conflicts
- Returns: conflict list with resolution options
```

### 4.2 Internal Agent APIs
Each agent exposes a standardized MCP interface:

```python
class AgentInterface:
    async def process_message(self, message: MCPMessage) -> MCPMessage:
        """Process incoming MCP messages"""

    async def health_check(self) -> dict:
        """Agent health status"""

    async def get_capabilities(self) -> list:
        """List of supported operations"""
```

## 5. User Interface Design

### 5.1 Chatbot Interface
**Main Components:**
- Message history panel
- Input field with command suggestions
- File upload area
- Status indicators
- Conflict resolution dialogs

**UI States:**
- Idle: Ready for input
- Processing: Showing progress indicators
- Conflict Resolution: Presenting options
- Error: Displaying error messages with suggestions

### 5.2 Responsive Design
- Mobile-first approach
- Progressive enhancement for larger screens
- Accessible design (WCAG 2.1 AA compliance)
- Dark/light theme support

### 5.3 Interaction Patterns
- Conversational flow with context awareness
- Progressive disclosure for complex operations
- Confirmation dialogs for destructive actions
- Inline help and command examples

## 6. Data Flow Diagrams

### 6.1 Schedule Upload Flow
```
1. User uploads file → Web Interface
2. Web Interface → Orchestrator (file metadata)
3. Orchestrator → Parsing Agent (file processing)
4. Parsing Agent → OpenAI Vision API (content extraction)
5. Parsing Agent → Orchestrator (structured events)
6. Orchestrator → Conflict Evaluation Agent (conflict check)
7. Conflict Evaluation Agent → Orchestrator (resolution options)
8. Orchestrator → Web Interface (user choice required)
9. User selects resolution → Web Interface
10. Web Interface → Orchestrator → Calendar Agent (create events)
11. Calendar Agent → Google Calendar API
```

### 6.2 Natural Language Command Flow
```
1. User types command → Web Interface
2. Web Interface → Orchestrator
3. Orchestrator → Change Management Agent
4. Change Management Agent → OpenAI Chat API (command interpretation)
5. Change Management Agent → Orchestrator (parsed command)
6. Orchestrator → Calendar Agent (current events query)
7. Calendar Agent → Google Calendar API
8. Orchestrator → Conflict Evaluation Agent (if needed)
9. Conflict Evaluation Agent → Orchestrator (resolution options)
10. Orchestrator → Calendar Agent (execute changes)
11. Calendar Agent → Google Calendar API
12. Orchestrator → Web Interface (confirmation)
```

## 7. Implementation Approach

### 7.1 Development Phases
**Phase 1: Foundation (Week 1-2)**
- Set up project structure and dependencies
- Implement basic agent framework and MCP
- Create web interface skeleton
- Set up API integrations (Google Calendar, OpenAI)

**Phase 2: Core Agents (Week 3-4)**
- Implement Parsing Agent with file processing
- Implement Calendar Agent with Google API integration
- Basic conflict detection
- Simple natural language parsing

**Phase 3: Advanced Features (Week 5-6)**
- Complete NLP integration
- Advanced conflict resolution
- Bulk operations support
- Error handling and recovery

**Phase 4: Testing & Polish (Week 7-8)**
- Comprehensive testing
- UI/UX improvements
- Documentation
- Performance optimization

### 7.2 Technology Stack Details
- **Backend**: Python 3.11+, FastAPI for web framework
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla or minimal framework)
- **Database**: No persistent storage (Google Calendar only)
- **APIs**: Google Calendar API v3, OpenAI API
- **MCP Implementation**: Custom JSON-based protocol
- **File Processing**: PyPDF2, openpyxl, pytesseract, PIL
- **Testing**: pytest, pytest-asyncio, unittest.mock

### 7.3 Project Structure
```
calendar_agents/
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── parsing_agent.py
│   ├── calendar_agent.py
│   ├── change_management_agent.py
│   └── conflict_evaluation_agent.py
├── core/
│   ├── mcp.py
│   ├── models.py
│   └── utils.py
├── api/
│   ├── __init__.py
│   ├── routes.py
│   └── dependencies.py
├── ui/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── config/
│   ├── settings.py
│   └── .env.example
└── main.py
```

## 8. Security Considerations

### 8.1 API Key Management
- API keys stored in environment variables
- Service account authentication for Google Calendar
- Rate limiting on OpenAI API calls
- Input validation and sanitization

### 8.2 Data Privacy
- No user data persistence
- Temporary file processing only
- Secure file upload handling
- HTTPS-only communication

### 8.3 Error Handling
- Sensitive information not exposed in error messages
- Graceful degradation on API failures
- User-friendly error messages
- Logging without PII exposure

## 9. Performance Considerations

### 9.1 Optimization Strategies
- Asynchronous processing for file uploads
- Caching for frequently accessed calendar data
- Batch operations for bulk updates
- Connection pooling for API calls

### 9.2 Scalability
- Stateless agent design
- Horizontal scaling capability
- Resource monitoring and alerts
- Performance profiling and optimization

## 10. Deployment Design

### 10.1 Environment Setup
- Docker containerization
- Environment-specific configurations
- Health check endpoints
- Graceful shutdown handling

### 10.2 Monitoring and Logging
- Structured logging with correlation IDs
- Performance metrics collection
- Error tracking and alerting
- Usage analytics (non-PII)

### 10.3 Backup and Recovery
- Configuration backup
- API key rotation procedures
- Incident response plan
- Rollback procedures

## 11. Testing Strategy

### 11.1 Unit Testing
- Agent logic testing
- API integration mocking
- Data validation testing
- Error condition handling

### 11.2 Integration Testing
- Agent communication via MCP
- End-to-end file processing
- Calendar API integration
- NLP command processing

### 11.3 User Acceptance Testing
- Real schedule file processing
- Natural language command testing
- Conflict resolution workflows
- UI/UX validation

## 12. Risk Assessment and Mitigation

### 12.1 Technical Risks
- **API Rate Limits**: Implement exponential backoff and request queuing
- **File Processing Errors**: Comprehensive error handling and fallback options
- **NLP Accuracy**: Human-in-the-loop validation for complex commands
- **Calendar Sync Issues**: Regular sync verification and manual override options

### 12.2 Business Risks
- **Scope Creep**: Strict adherence to requirements and phased delivery
- **Integration Failures**: Early prototyping and testing of all API integrations
- **Performance Issues**: Performance testing and optimization from day one

### 12.3 Mitigation Strategies
- Regular code reviews and pair programming
- Comprehensive testing at all levels
- Clear communication and expectation management
- Incremental delivery with working prototypes

## 13. Success Metrics

### 13.1 Functional Metrics
- Schedule parsing accuracy (>95%)
- NLP command understanding (>90%)
- Conflict detection rate (100%)
- Calendar sync reliability (99.9%)

### 13.2 Performance Metrics
- File processing time (<30 seconds)
- Command response time (<5 seconds)
- System uptime (>99%)
- API error rate (<1%)

### 13.3 User Experience Metrics
- Task completion rate
- Error recovery success rate
- User satisfaction scores
- Feature adoption rates

This design document provides a comprehensive blueprint for implementing the Agentic Scheduler system, ensuring all requirements are met while maintaining architectural clarity and implementation feasibility.
