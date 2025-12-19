"""API endpoints for User table operations using Reflex ORM."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import reflex as rx
from ...models.models import User

app = FastAPI()

class UserCreate(BaseModel):
    telegram_id: str
    username: str
    first_name: str
    last_name: str
    balance: float = 0.0
    total_spent: float = 0.0
    status: str = "active"
    risk_score: float = 0.0

class UserResponse(BaseModel):
    id: int
    telegram_id: str
    username: str
    first_name: str
    last_name: str
    balance: float
    total_spent: float
    status: str
    created_at: datetime
    updated_at: datetime
    last_activity: Optional[datetime] = None
    risk_score: float

def register_user_routes(fastapi_app: FastAPI):
    """Register user API routes with the FastAPI app."""
    
    @fastapi_app.post("/api/users", response_model=UserResponse)
    async def create_user(user: UserCreate):
        """Create a new user."""
        try:
            with rx.session() as session:
                new_user = User(
                    telegram_id=user.telegram_id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    balance=user.balance,
                    total_spent=user.total_spent,
                    status=user.status,
                    risk_score=user.risk_score,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                
                return UserResponse(
                    id=new_user.id,
                    telegram_id=new_user.telegram_id,
                    username=new_user.username,
                    first_name=new_user.first_name,
                    last_name=new_user.last_name,
                    balance=new_user.balance,
                    total_spent=new_user.total_spent,
                    status=new_user.status,
                    created_at=new_user.created_at,
                    updated_at=new_user.updated_at,
                    last_activity=new_user.last_activity,
                    risk_score=new_user.risk_score
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    @fastapi_app.get("/api/users", response_model=list[UserResponse])
    async def get_all_users():
        """Get all users."""
        try:
            with rx.session() as session:
                users = session.query(User).all()
                return [
                    UserResponse(
                        id=user.id,
                        telegram_id=user.telegram_id,
                        username=user.username,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        balance=user.balance,
                        total_spent=user.total_spent,
                        status=user.status,
                        created_at=user.created_at,
                        updated_at=user.updated_at,
                        last_activity=user.last_activity,
                        risk_score=user.risk_score
                    )
                    for user in users
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

    @fastapi_app.get("/api/users/{telegram_id}", response_model=UserResponse)
    async def get_user_by_telegram_id(telegram_id: str):
        """Get user by telegram_id."""
        try:
            with rx.session() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if not user:
                    raise HTTPException(status_code=404, detail=f"User with telegram_id '{telegram_id}' not found")
                
                return UserResponse(
                    id=user.id,
                    telegram_id=user.telegram_id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    balance=user.balance,
                    total_spent=user.total_spent,
                    status=user.status,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    last_activity=user.last_activity,
                    risk_score=user.risk_score
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

    @fastapi_app.put("/api/users/{telegram_id}", response_model=UserResponse)
    async def update_user(telegram_id: str, user: UserCreate):
        """Update user by telegram_id."""
        try:
            with rx.session() as session:
                existing_user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if not existing_user:
                    raise HTTPException(status_code=404, detail=f"User with telegram_id '{telegram_id}' not found")
                
                existing_user.username = user.username
                existing_user.first_name = user.first_name
                existing_user.last_name = user.last_name
                existing_user.balance = user.balance
                existing_user.total_spent = user.total_spent
                existing_user.status = user.status
                existing_user.risk_score = user.risk_score
                existing_user.updated_at = datetime.utcnow()
                session.commit()
                session.refresh(existing_user)
                
                return UserResponse(
                    id=existing_user.id,
                    telegram_id=existing_user.telegram_id,
                    username=existing_user.username,
                    first_name=existing_user.first_name,
                    last_name=existing_user.last_name,
                    balance=existing_user.balance,
                    total_spent=existing_user.total_spent,
                    status=existing_user.status,
                    created_at=existing_user.created_at,
                    updated_at=existing_user.updated_at,
                    last_activity=existing_user.last_activity,
                    risk_score=existing_user.risk_score
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

    @fastapi_app.delete("/api/users/{telegram_id}")
    async def delete_user(telegram_id: str):
        """Delete user by telegram_id."""
        try:
            with rx.session() as session:
                user = session.query(User).filter(User.telegram_id == telegram_id).first()
                if not user:
                    raise HTTPException(status_code=404, detail=f"User with telegram_id '{telegram_id}' not found")
                
                session.delete(user)
                session.commit()
                return {"message": f"User with telegram_id '{telegram_id}' deleted successfully"}
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")