"""API endpoints for BotLog table operations using Reflex ORM."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import reflex as rx
from ...models.models import BotLog

app = FastAPI()

class BotLogCreate(BaseModel):
    level: str  # info, warning, error, debug
    message: str
    user_id: Optional[str] = None
    extra_data: Optional[str] = None

class BotLogResponse(BaseModel):
    id: int
    level: str
    message: str
    timestamp: datetime
    user_id: Optional[str] = None
    extra_data: Optional[str] = None

def register_botlogs_routes(fastapi_app: FastAPI):
    """Register bot log API routes with the FastAPI app."""
    
    @fastapi_app.post("/api/botlogs", response_model=BotLogResponse)
    async def create_botlog(log: BotLogCreate):
        """Create a new bot log entry."""
        try:
            with rx.session() as session:
                new_log = BotLog(
                    level=log.level,
                    message=log.message,
                    user_id=log.user_id,
                    extra_data=log.extra_data,
                    timestamp=datetime.utcnow()
                )
                session.add(new_log)
                session.commit()
                session.refresh(new_log)
                
                return BotLogResponse(
                    id=new_log.id,
                    level=new_log.level,
                    message=new_log.message,
                    timestamp=new_log.timestamp,
                    user_id=new_log.user_id,
                    extra_data=new_log.extra_data
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating bot log: {str(e)}")

    @fastapi_app.get("/api/botlogs", response_model=list[BotLogResponse])
    async def get_all_botlogs():
        """Get all bot log entries."""
        try:
            with rx.session() as session:
                logs = session.query(BotLog).all()
                return [
                    BotLogResponse(
                        id=log.id,
                        level=log.level,
                        message=log.message,
                        timestamp=log.timestamp,
                        user_id=log.user_id,
                        extra_data=log.extra_data
                    )
                    for log in logs
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching bot logs: {str(e)}")

    @fastapi_app.get("/api/botlogs/{log_id}", response_model=BotLogResponse)
    async def get_botlog_by_id(log_id: int):
        """Get bot log by ID."""
        try:
            with rx.session() as session:
                log = session.query(BotLog).filter(BotLog.id == log_id).first()
                if not log:
                    raise HTTPException(status_code=404, detail=f"Bot log with ID '{log_id}' not found")
                
                return BotLogResponse(
                    id=log.id,
                    level=log.level,
                    message=log.message,
                    timestamp=log.timestamp,
                    user_id=log.user_id,
                    extra_data=log.extra_data
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching bot log: {str(e)}")

    @fastapi_app.get("/api/botlogs/user/{user_id}", response_model=list[BotLogResponse])
    async def get_botlogs_by_user(user_id: str):
        """Get all bot log entries for a specific user."""
        try:
            with rx.session() as session:
                logs = session.query(BotLog).filter(BotLog.user_id == user_id).all()
                return [
                    BotLogResponse(
                        id=log.id,
                        level=log.level,
                        message=log.message,
                        timestamp=log.timestamp,
                        user_id=log.user_id,
                        extra_data=log.extra_data
                    )
                    for log in logs
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user bot logs: {str(e)}")

    @fastapi_app.get("/api/botlogs/level/{level}", response_model=list[BotLogResponse])
    async def get_botlogs_by_level(level: str):
        """Get all bot log entries by level."""
        try:
            with rx.session() as session:
                logs = session.query(BotLog).filter(BotLog.level == level).all()
                return [
                    BotLogResponse(
                        id=log.id,
                        level=log.level,
                        message=log.message,
                        timestamp=log.timestamp,
                        user_id=log.user_id,
                        extra_data=log.extra_data
                    )
                    for log in logs
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching bot logs by level: {str(e)}")

    @fastapi_app.delete("/api/botlogs/{log_id}")
    async def delete_botlog(log_id: int):
        """Delete bot log by ID."""
        try:
            with rx.session() as session:
                log = session.query(BotLog).filter(BotLog.id == log_id).first()
                if not log:
                    raise HTTPException(status_code=404, detail=f"Bot log with ID '{log_id}' not found")
                
                session.delete(log)
                session.commit()
                return {"message": f"Bot log with ID '{log_id}' deleted successfully"}
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting bot log: {str(e)}")

    @fastapi_app.delete("/api/botlogs/user/{user_id}")
    async def delete_botlogs_by_user(user_id: str):
        """Delete all bot log entries for a specific user."""
        try:
            with rx.session() as session:
                logs = session.query(BotLog).filter(BotLog.user_id == user_id).all()
                for log in logs:
                    session.delete(log)
                session.commit()
                return {"message": f"All bot logs for user '{user_id}' deleted successfully"}
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting user bot logs: {str(e)}")