"""
Agentic Scheduler - Main Application Entry Point
"""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import router as api_router
from config.settings import settings

# Create FastAPI application
app = FastAPI(
    title="Agentic Scheduler",
    description="A chatbot-based calendar management system",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# Include API routes
app.include_router(api_router, prefix="/api")

# Setup templates
templates = Jinja2Templates(directory="ui/templates")


@app.get("/")
async def root():
    """Root endpoint - redirects to chatbot interface"""
    return {"message": "Agentic Scheduler API", "docs": "/docs", "chat": "/chat"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        log_level="info"
    )
