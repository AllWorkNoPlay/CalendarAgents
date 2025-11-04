"""
Integration tests for file upload functionality
"""
import pytest


@pytest.mark.integration
class TestFileUpload:
    """Test file upload endpoints"""

    @pytest.fixture(autouse=True)
    def setup_method(self, test_client):
        """Setup test client"""
        self.client = test_client

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "System is healthy" in data["message"]

    def test_agents_endpoint(self):
        """Test agents listing endpoint"""
        response = self.client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "agents" in data["data"]

    def test_chat_endpoint_get(self):
        """Test chat endpoint GET request"""
        response = self.client.post("/api/chat", json={"message": "Hello", "message_type": "user"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "message" in data

    def test_upload_empty_file(self):
        """Test upload with empty file"""
        files = {"file": ("empty.txt", b"", "text/plain")}
        response = self.client.post("/api/upload", files=files)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "No file provided" in data["message"]

    def test_upload_text_file(self):
        """Test upload with sample text file"""
        sample_content = b"Mathematics 101 - Monday 9:00 AM - Room 101\nPhysics Lab - Tuesday 2:00 PM - Lab 205"
        files = {"file": ("sample.txt", sample_content, "text/plain")}

        response = self.client.post("/api/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "sample.txt" in data["message"]
        assert "events_found" in data["data"]
        assert "events_created" in data["data"]
