/**
 * Agentic Scheduler Chat Interface JavaScript
 */

class ChatInterface {
    constructor() {
        this.messageCount = 0;
        this.isUploading = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.showWelcomeMessage();
    }

    bindEvents() {
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');

        // Enter key to send message
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Send button click
        sendBtn.addEventListener('click', () => this.sendMessage());

        // File upload
        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.handleFileSelection(e.target.files[0]);
        });
    }

    showWelcomeMessage() {
        this.addMessage(
            "Hello! I'm your AI scheduling assistant. I can help you manage your calendar through natural language commands. Try saying things like:<br><br>" +
            "• 'Add a meeting tomorrow at 3 PM'<br>" +
            "• 'Show me my schedule for Friday'<br>" +
            "• 'Upload a schedule' (use the upload button above)<br><br>" +
            "Full features will be available in future sprints!",
            'system'
        );
    }

    addMessage(content, type = 'system', isHtml = false) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        if (isHtml) {
            contentDiv.innerHTML = content;
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        this.messageCount++;
        return messageDiv;
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();

        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();

        try {
            const response = await this.apiCall('/api/chat', {
                message: message,
                message_type: 'user',
                timestamp: new Date().toISOString()
            });

            // Remove typing indicator
            typingIndicator.remove();

            if (response.success) {
                this.addMessage(response.message, 'system');
                this.showStatus('Message sent successfully', 'success');
            } else {
                this.addMessage(`Sorry, I encountered an error: ${response.message}`, 'system');
                this.showStatus('Failed to send message', 'error');
            }
        } catch (error) {
            typingIndicator.remove();
            this.addMessage('Network error. Please try again.', 'system');
            this.showStatus('Network error', 'error');
            console.error('Chat error:', error);
        }
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const indicator = document.createElement('div');
        indicator.className = 'message system-message typing';
        indicator.innerHTML = `
            <div class="message-content">
                <span class="loading"></span> Thinking...
            </div>
        `;
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return indicator;
    }

    async uploadFile() {
        const fileInput = document.getElementById('fileInput');
        const uploadBtn = document.getElementById('uploadBtn');
        const file = fileInput.files[0];

        if (!file) {
            this.showStatus('Please select a file first', 'error');
            return;
        }

        if (this.isUploading) {
            this.showStatus('Upload already in progress', 'error');
            return;
        }

        // Validate file type
        const allowedTypes = ['pdf', 'xlsx', 'xls', 'png', 'jpg', 'jpeg', 'gif'];
        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (!allowedTypes.includes(fileExtension)) {
            this.showStatus(`File type not supported. Allowed: ${allowedTypes.join(', ')}`, 'error');
            return;
        }

        // Validate file size (10MB limit)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            this.showStatus('File too large. Maximum size: 10MB', 'error');
            return;
        }

        this.isUploading = true;
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<span class="loading"></span> Uploading...';

        // Add upload message
        this.addMessage(`Uploading ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)...`, 'user');

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.addMessage(
                    `✅ Successfully processed ${file.name}.<br><br>${data.message}`,
                    'system',
                    true
                );
                this.showStatus('File uploaded successfully!', 'success');
            } else {
                this.addMessage(`❌ Failed to process file: ${data.message}`, 'system');
                this.showStatus('Upload failed', 'error');
            }
        } catch (error) {
            this.addMessage('Upload failed due to network error.', 'system');
            this.showStatus('Upload failed', 'error');
            console.error('Upload error:', error);
        } finally {
            this.isUploading = false;
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload Schedule';
            fileInput.value = ''; // Clear file input
        }
    }

    handleFileSelection(file) {
        if (file) {
            const fileInfo = document.createElement('div');
            fileInfo.className = 'file-info';
            fileInfo.textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            // You could display this info somewhere in the UI
        }
    }

    showStatus(message, type = 'info') {
        const statusEl = document.getElementById('statusMessage');
        statusEl.textContent = message;
        statusEl.className = `status-message ${type}`;
        statusEl.style.display = 'block';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            statusEl.style.display = 'none';
        }, 5000);
    }

    async apiCall(endpoint, data) {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatInterface = new ChatInterface();
});

// Make uploadFile function globally available for the HTML button
window.uploadFile = function() {
    if (window.chatInterface) {
        window.chatInterface.uploadFile();
    }
};
