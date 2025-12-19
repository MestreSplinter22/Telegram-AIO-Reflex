"""
Template for creating new API endpoints.

To create a new API module:
1. Copy this file to a new folder (e.g., users, products, etc.)
2. Rename it to __init__.py
3. Update the register_routes function name and implementation
4. Add your specific endpoints
"""

from fastapi import FastAPI, HTTPException
from typing import Optional, List


def register_template_routes(app: FastAPI):
    """Register template API routes."""
    
    @app.get("/api/template")
    async def get_template():
        """Example GET endpoint."""
        return {"message": "Template GET endpoint", "status": "success"}
    
    @app.post("/api/template")
    async def create_template(item: dict):
        """Example POST endpoint."""
        return {"message": "Template POST endpoint", "data": item}
    
    @app.put("/api/template/{item_id}")
    async def update_template(item_id: int, item: dict):
        """Example PUT endpoint."""
        return {"message": f"Updated item {item_id}", "data": item}
    
    @app.delete("/api/template/{item_id}")
    async def delete_template(item_id: int):
        """Example DELETE endpoint."""
        return {"message": f"Deleted item {item_id}"}


# Example usage in main app:
# from .backend.api.template import register_template_routes
# register_template_routes(fastapi_app)