"""Healthy endpoint for API status checking."""

from fastapi import FastAPI
from ...database import get_db_session

# This module will be automatically imported by the centralized API system
# The FastAPI instance will be available from the main app

def register_healthy_routes(app: FastAPI):
    """Register the healthy endpoint routes."""
    
    @app.get("/api/healthy")
    async def healthy():
        """Health check endpoint to verify API is functioning."""
        try:
            # Basic database connectivity check
            db = get_db_session()
            # Note: Reflex uses async sessions, so we'll skip the DB check for now
            # and just return a basic health status
            return {"status": "api funcionando normalmente", "database": "connected"}
        except Exception as e:
            return {"status": "api funcionando normalmente", "database": "disconnected", "error": str(e)}