# Agentic Scheduler

An AI-powered calendar management system that converts static class schedules into dynamic Google Calendar events using natural language processing and agent-based architecture.

## 🎯 Project Overview

This system provides a chatbot-style web interface for:
- **Schedule Upload**: Convert PDF, Excel, and image schedules to calendar events
- **Natural Language Management**: Control your calendar with conversational commands
- **Conflict Detection**: Automatically detect and resolve scheduling conflicts
- **Multi-Agent Architecture**: Modular design with specialized agents communicating via MCP

## 🚀 Sprint Status

### ✅ Sprint 1: Foundation & Infrastructure (COMPLETED)
- ✅ Project structure with agents/, core/, api/, ui/ directories
- ✅ FastAPI web server with basic endpoints
- ✅ Chatbot interface accessible via browser
- ✅ MCP (Model Context Protocol) implementation
- ✅ Agent framework with base classes
- ✅ Health check and monitoring endpoints
- ✅ Unit tests for core components

### 🔄 Sprint 2: File Parsing & Calendar Integration (NEXT)
- File upload handling for PDF, Excel, images
- Google Calendar API integration
- Parsing Agent implementation
- Calendar Agent implementation

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calendar-agents
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Option 1: Smart installer (recommended for Python 3.13)
   python3 install.py

   # Option 2: Manual installation
   # For Python 3.11-3.12:
   pip install -r requirements.txt

   # For Python 3.13 (recommended):
   pip install -r requirements-py313.txt

   # For minimal setup (only Sprint 1):
   pip install -r requirements-minimal.txt
   ```

4. **Environment configuration**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your API keys
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the application**
   - Open your browser to `http://localhost:8000`
   - Chat interface: `http://localhost:8000/chat`
   - API documentation: `http://localhost:8000/docs`

### Troubleshooting Python 3.13

If you encounter installation issues with Python 3.13:

1. **Use Python 3.13 specific requirements:**
   ```bash
   pip install -r requirements-py313.txt
   ```

2. **Upgrade pip first:**
   ```bash
   pip install --upgrade pip
   ```

3. **Install in user space if permission issues:**
   ```bash
   pip install --user -r requirements-py313.txt
   ```

4. **Check for conflicting packages:**
   ```bash
   pip check
   ```

5. **Alternative: Use minimal requirements for testing:**
   ```bash
   pip install -r requirements-minimal.txt
   ```

### Configuration

Edit `config/.env` with your API credentials:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Calendar API Configuration
GOOGLE_CALENDAR_API_KEY=your_google_calendar_api_key_here
GOOGLE_CALENDAR_ID=your_google_calendar_id_here

# Server Configuration
PORT=8000
HOST=0.0.0.0

# Environment
ENVIRONMENT=development
DEBUG=true
```

## 🏗️ Project Structure

```
calendar_agents/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent classes
│   ├── orchestrator.py    # Orchestrator agent
│   ├── parsing_agent.py   # File parsing agent (Sprint 2)
│   ├── calendar_agent.py  # Calendar integration agent (Sprint 2)
│   └── ...
├── core/                  # Core functionality
│   ├── mcp.py            # Model Context Protocol
│   ├── models.py         # Data models
│   └── utils.py          # Utility functions
├── api/                   # API endpoints
│   ├── __init__.py
│   ├── routes.py         # API routes
│   └── dependencies.py   # API dependencies
├── ui/                    # User interface
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
├── tests/                 # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── config/                # Configuration
│   ├── settings.py       # Settings management
│   └── .env.example      # Environment template
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=core --cov=agents --cov=api
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with service info
- `GET /chat` - Chatbot interface
- `GET /health` - Health check
- `GET /docs` - API documentation

### Chat Endpoints
- `POST /api/chat` - Send chat messages
- `POST /api/upload` - Upload schedule files
- `GET /api/agents` - List registered agents

## 🤖 Agent Architecture

The system uses a multi-agent architecture with specialized agents:

### Current Agents (Sprint 1)
- **Orchestrator Agent**: Coordinates all other agents
- **Mock Agents**: Placeholder agents for testing

### Planned Agents
- **Parsing Agent**: Handles file parsing and data extraction
- **Calendar Agent**: Manages Google Calendar integration
- **Change Management Agent**: Processes natural language commands
- **Conflict Evaluation Agent**: Detects and resolves conflicts

### Communication
Agents communicate using the **Model Context Protocol (MCP)** with JSON messages.

## 🔧 Development Guidelines

### Code Style
- Use Black for code formatting
- Use isort for import sorting
- Follow PEP 8 conventions
- Write comprehensive docstrings

### Testing
- Write unit tests for all new functionality
- Aim for >80% code coverage
- Use pytest fixtures for test data
- Test both success and error scenarios

### Git Workflow
- Use feature branches for new development
- Write clear commit messages
- Create pull requests for code review
- Keep commits focused and atomic

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
```bash
# Set environment to production
ENVIRONMENT=production python main.py
```

### Docker Deployment (Future)
```bash
docker build -t calendar-agents .
docker run -p 8000:8000 calendar-agents
```

## 📋 Sprint Backlog

### Sprint 2: File Parsing & Calendar Integration
- [ ] Implement PDF parsing with PyPDF2
- [ ] Implement Excel parsing with openpyxl
- [ ] Implement OCR for images with Tesseract
- [ ] Create Parsing Agent
- [ ] Implement Google Calendar API integration
- [ ] Create Calendar Agent
- [ ] Add comprehensive file validation
- [ ] Update UI for file upload feedback

### Sprint 3: Natural Language Processing
- [ ] Implement OpenAI Chat Completions integration
- [ ] Create Change Management Agent
- [ ] Add command parsing and validation
- [ ] Implement basic NLP command recognition
- [ ] Add command confirmation dialogs
- [ ] Enhance chatbot interface

### Sprint 4: Conflict Detection & Resolution
- [ ] Implement conflict detection algorithms
- [ ] Create Conflict Evaluation Agent
- [ ] Add resolution option generation
- [ ] Implement school year constraints
- [ ] Add conflict resolution UI
- [ ] Test complex conflict scenarios

### Sprint 5: System Integration & Advanced Features
- [ ] Complete Orchestrator Agent implementation
- [ ] Add recurring event support
- [ ] Implement bulk operations
- [ ] Add comprehensive error handling
- [ ] Performance optimization
- [ ] End-to-end testing

### Sprint 6: Testing, Polish & Deployment
- [ ] Comprehensive test suite
- [ ] UI/UX polish and mobile responsiveness
- [ ] Documentation completion
- [ ] Deployment scripts and configuration
- [ ] Final security review
- [ ] Production deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is part of an educational assignment and is not licensed for commercial use.

## 📞 Support

For questions or issues, please check the current sprint status and documentation. Full features will be implemented incrementally across the sprint cycle.

---

**Current Version**: Sprint 1 Complete
**Next Sprint**: Sprint 2 - File Parsing & Calendar Integration
**Estimated Completion**: End of Sprint 6
