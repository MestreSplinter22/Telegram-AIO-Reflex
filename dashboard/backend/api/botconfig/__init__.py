"""API endpoints for BotConfig table operations using Reflex ORM."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import reflex as rx
from ...models.models import BotConfig


class BotConfigCreate(BaseModel):
    """Schema for creating a new BotConfig entry."""
    key: str
    value: str
    description: str = None


class BotConfigResponse(BaseModel):
    """Schema for BotConfig response."""
    id: int
    key: str
    value: str
    description: str = None
    updated_at: datetime


def register_botconfig_routes(app: FastAPI):
    """Register BotConfig API routes."""
    
    @app.post("/api/botconfig", response_model=BotConfigResponse)
    async def create_botconfig(config: BotConfigCreate):
        """Create a new BotConfig entry."""
        try:
            with rx.session() as session:
                # Create new BotConfig instance
                new_config = BotConfig(
                    key=config.key,
                    value=config.value,
                    description=config.description,
                    updated_at=datetime.utcnow()
                )
                session.add(new_config)
                session.commit()
                session.refresh(new_config)
                
                return BotConfigResponse(
                    id=new_config.id,
                    key=new_config.key,
                    value=new_config.value,
                    description=new_config.description,
                    updated_at=new_config.updated_at
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating BotConfig: {str(e)}")
    
    @app.get("/api/botconfig", response_model=list[BotConfigResponse])
    async def get_all_botconfigs():
        """Get all BotConfig entries."""
        try:
            with rx.session() as session:
                configs = session.query(BotConfig).all()
                return [
                    BotConfigResponse(
                        id=config.id,
                        key=config.key,
                        value=config.value,
                        description=config.description,
                        updated_at=config.updated_at
                    )
                    for config in configs
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching BotConfigs: {str(e)}")

    @app.get("/api/botconfig/{key}", response_model=BotConfigResponse)
    async def get_botconfig_by_key(key: str):
        """Get BotConfig by key."""
        try:
            with rx.session() as session:
                config = session.query(BotConfig).filter(BotConfig.key == key).first()
                if not config:
                    raise HTTPException(status_code=404, detail=f"BotConfig with key '{key}' not found")
                
                return BotConfigResponse(
                    id=config.id,
                    key=config.key,
                    value=config.value,
                    description=config.description,
                    updated_at=config.updated_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching BotConfig: {str(e)}")
    
    @app.put("/api/botconfig/{key}", response_model=BotConfigResponse)
    async def update_botconfig(key: str, config: BotConfigCreate):
        """Update BotConfig by key."""
        try:
            with rx.session() as session:
                existing_config = session.query(BotConfig).filter(BotConfig.key == key).first()
                if not existing_config:
                    raise HTTPException(status_code=404, detail=f"BotConfig with key '{key}' not found")
                
                existing_config.value = config.value
                existing_config.description = config.description
                existing_config.updated_at = datetime.utcnow()
                session.commit()
                session.refresh(existing_config)
                
                return BotConfigResponse(
                    id=existing_config.id,
                    key=existing_config.key,
                    value=existing_config.value,
                    description=existing_config.description,
                    updated_at=existing_config.updated_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating BotConfig: {str(e)}")

    @app.delete("/api/botconfig/{key}")
    async def delete_botconfig(key: str):
        """Delete BotConfig by key."""
        try:
            with rx.session() as session:
                config = session.query(BotConfig).filter(BotConfig.key == key).first()
                if not config:
                    raise HTTPException(status_code=404, detail=f"BotConfig with key '{key}' not found")
                
                session.delete(config)
                session.commit()
                return {"message": f"BotConfig with key '{key}' deleted successfully"}
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting BotConfig: {str(e)}")