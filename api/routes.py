"""
API routes for the Agentic Scheduler
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse

from core.mcp import message_bus, send_message_to_agent
from core.models import APIResponse, ChatMessage
from agents.orchestrator import OrchestratorAgent

from .dependencies import get_orchestrator

router = APIRouter()


@router.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Serve the chat interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agentic Scheduler</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .chat-container {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .chat-messages {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                margin-bottom: 20px;
                background: #fafafa;
                border-radius: 5px;
            }
            .message {
                margin-bottom: 10px;
                padding: 8px;
                border-radius: 5px;
            }
            .user-message {
                background: #007bff;
                color: white;
                text-align: right;
            }
            .system-message {
                background: #28a745;
                color: white;
            }
            .input-group {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
            .file-upload {
                margin-bottom: 20px;
            }
            .status {
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                display: none;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>🤖 Agentic Scheduler</h1>
            <p>Welcome to your AI-powered calendar assistant!</p>

            <div class="file-upload">
                <h3>Upload Schedule</h3>
                <input type="file" id="fileInput" accept=".pdf,.xlsx,.xls,.png,.jpg,.jpeg,.gif">
                <button onclick="uploadFile()">Upload Schedule</button>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message system-message">
                    Hello! I'm your scheduling assistant. You can upload a schedule file above, or chat with me using natural language commands like "add a meeting tomorrow at 3 PM" or "show me my schedule for Friday".
                </div>
            </div>

            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>

            <div id="status" class="status"></div>
        </div>

        <script>
            let messageCount = 1;

            function addMessage(text, type = 'system') {
                const messages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                messageDiv.textContent = text;
                messages.appendChild(messageDiv);
                messages.scrollTop = messages.scrollHeight;
                messageCount++;
            }

            function showStatus(message, type = 'success') {
                const status = document.getElementById('status');
                status.textContent = message;
                status.className = `status ${type}`;
                status.style.display = 'block';
                setTimeout(() => {
                    status.style.display = 'none';
                }, 5000);
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();

                if (!message) return;

                addMessage(message, 'user');
                input.value = '';

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });

                    const data = await response.json();

                    if (data.success) {
                        addMessage(data.message, 'system');
                    } else {
                        addMessage('Sorry, I encountered an error: ' + data.message, 'system');
                    }
                } catch (error) {
                    addMessage('Network error. Please try again.', 'system');
                    console.error('Chat error:', error);
                }
            }

            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];

                if (!file) {
                    showStatus('Please select a file first', 'error');
                    return;
                }

                const formData = new FormData();
                formData.append('file', file);

                try {
                    addMessage(`Uploading ${file.name}...`, 'user');

                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (data.success) {
                        addMessage(`✅ Successfully processed ${file.name}. ${data.message}`, 'system');
                        showStatus('File uploaded successfully!', 'success');
                    } else {
                        addMessage(`❌ Failed to process file: ${data.message}`, 'system');
                        showStatus('Upload failed', 'error');
                    }
                } catch (error) {
                    addMessage('Upload failed due to network error.', 'system');
                    showStatus('Upload failed', 'error');
                    console.error('Upload error:', error);
                }

                // Clear file input
                fileInput.value = '';
            }

            // Initialize with a welcome message
            document.addEventListener('DOMContentLoaded', function() {
                addMessage('System ready! You can now upload schedule files or send chat messages.', 'system');
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post("/chat")
async def chat_endpoint(
    chat_message: ChatMessage,
    orchestrator: OrchestratorAgent = Depends(get_orchestrator)
):
    """Handle chat messages"""
    try:
        # For Sprint 1, just echo back with a mock response
        # In future sprints, this will route to the Change Management Agent
        response_message = f"I received your message: '{chat_message.message}'. This is a basic response - full NLP processing will be available in Sprint 3."

        return APIResponse(
            success=True,
            message=response_message,
            data={"message_type": "echo_response"}
        )

    except Exception as e:
        return APIResponse(
            success=False,
            message=f"Chat processing error: {str(e)}",
            errors=[str(e)]
        )


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    orchestrator: OrchestratorAgent = Depends(get_orchestrator)
):
    """Handle file uploads and process them"""
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Read file content
        file_content = await file.read()

        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file provided")

        # Route to Parsing Agent
        parsing_result = await orchestrator.coordinate_request(
            "parsing_agent",
            "parse_schedule",
            {
                "file_data": file_content,
                "filename": file.filename
            }
        )

        if parsing_result.get("status") != "success":
            return APIResponse(
                success=False,
                message=f"File parsing failed: {parsing_result.get('message', 'Unknown error')}",
                errors=["parsing_failed"]
            )

        events_data = parsing_result.get("events", [])

        if not events_data:
            return APIResponse(
                success=True,
                message=f"File '{filename}' processed successfully, but no events were found.",
                data={
                    "filename": filename,
                    "file_size": len(file),
                    "events_found": 0,
                    "parsing_result": parsing_result
                }
            )

        # Create events in calendar
        calendar_result = await orchestrator.coordinate_request(
            "calendar_agent",
            "create_events",
            {
                "events": events_data
            }
        )

        events_created = calendar_result.get("events_created", 0)

        return APIResponse(
            success=True,
            message=f"Successfully processed '{filename}' and created {events_created} calendar events!",
            data={
                "filename": filename,
                "file_size": len(file),
                "events_found": len(events_data),
                "events_created": events_created,
                "parsing_result": parsing_result,
                "calendar_result": calendar_result
            }
        )

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return APIResponse(
            success=False,
            message=f"Upload processing error: {str(e)}",
            errors=[str(e), error_details]
        )


@router.get("/health")
async def health_endpoint(orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    """Health check endpoint"""
    try:
        # Get orchestrator health
        health_data = await orchestrator.health_check()

        return APIResponse(
            success=True,
            message="System is healthy",
            data=health_data
        )

    except Exception as e:
        return APIResponse(
            success=False,
            message=f"Health check failed: {str(e)}",
            errors=[str(e)]
        )


@router.get("/agents")
async def list_agents_endpoint(orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    """List all registered agents"""
    try:
        # Request agent list from orchestrator
        result = await orchestrator.coordinate_request("orchestrator", "list_agents", {})

        return APIResponse(
            success=True,
            message=f"Found {result['total_count']} agents",
            data=result
        )

    except Exception as e:
        return APIResponse(
            success=False,
            message=f"Failed to list agents: {str(e)}",
            errors=[str(e)]
        )
