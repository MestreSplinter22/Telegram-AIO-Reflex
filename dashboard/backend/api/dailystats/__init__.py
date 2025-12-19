"""API endpoints for DailyStatistics table operations using Reflex ORM."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import reflex as rx
from ...models.models import DailyStatistics

app = FastAPI()

class DailyStatsCreate(BaseModel):
    date: str  # YYYY-MM-DD format
    total_revenue: float = 0.0
    total_users: int = 0
    active_users: int = 0
    total_transactions: int = 0
    total_gift_cards_sold: int = 0
    total_balance: float = 0.0
    bot_uptime: float = 0.0
    error_count: int = 0

class DailyStatsResponse(BaseModel):
    id: int
    date: str
    total_revenue: float
    total_users: int
    active_users: int
    total_transactions: int
    total_gift_cards_sold: int
    total_balance: float
    bot_uptime: float
    error_count: int
    created_at: datetime

def register_dailystats_routes(fastapi_app: FastAPI):
    """Register daily statistics API routes with the FastAPI app."""
    
    @fastapi_app.post("/api/dailystats", response_model=DailyStatsResponse)
    async def create_dailystats(stats: DailyStatsCreate):
        """Create a new daily statistics entry."""
        try:
            with rx.session() as session:
                new_stats = DailyStatistics(
                    date=stats.date,
                    total_revenue=stats.total_revenue,
                    total_users=stats.total_users,
                    active_users=stats.active_users,
                    total_transactions=stats.total_transactions,
                    total_gift_cards_sold=stats.total_gift_cards_sold,
                    total_balance=stats.total_balance,
                    bot_uptime=stats.bot_uptime,
                    error_count=stats.error_count,
                    created_at=datetime.utcnow()
                )
                session.add(new_stats)
                session.commit()
                session.refresh(new_stats)
                
                return DailyStatsResponse(
                    id=new_stats.id,
                    date=new_stats.date,
                    total_revenue=new_stats.total_revenue,
                    total_users=new_stats.total_users,
                    active_users=new_stats.active_users,
                    total_transactions=new_stats.total_transactions,
                    total_gift_cards_sold=new_stats.total_gift_cards_sold,
                    total_balance=new_stats.total_balance,
                    bot_uptime=new_stats.bot_uptime,
                    error_count=new_stats.error_count,
                    created_at=new_stats.created_at
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating daily stats: {str(e)}")

    @fastapi_app.get("/api/dailystats", response_model=list[DailyStatsResponse])
    async def get_all_dailystats():
        """Get all daily statistics."""
        try:
            with rx.session() as session:
                stats = session.query(DailyStatistics).all()
                return [
                    DailyStatsResponse(
                        id=stat.id,
                        date=stat.date,
                        total_revenue=stat.total_revenue,
                        total_users=stat.total_users,
                        active_users=stat.active_users,
                        total_transactions=stat.total_transactions,
                        total_gift_cards_sold=stat.total_gift_cards_sold,
                        total_balance=stat.total_balance,
                        bot_uptime=stat.bot_uptime,
                        error_count=stat.error_count,
                        created_at=stat.created_at
                    )
                    for stat in stats
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching daily stats: {str(e)}")

    @fastapi_app.get("/api/dailystats/{date}", response_model=DailyStatsResponse)
    async def get_dailystats_by_date(date: str):
        """Get daily statistics by date (YYYY-MM-DD)."""
        try:
            with rx.session() as session:
                stats = session.query(DailyStatistics).filter(DailyStatistics.date == date).first()
                if not stats:
                    raise HTTPException(status_code=404, detail=f"Daily stats for date '{date}' not found")
                
                return DailyStatsResponse(
                    id=stats.id,
                    date=stats.date,
                    total_revenue=stats.total_revenue,
                    total_users=stats.total_users,
                    active_users=stats.active_users,
                    total_transactions=stats.total_transactions,
                    total_gift_cards_sold=stats.total_gift_cards_sold,
                    total_balance=stats.total_balance,
                    bot_uptime=stats.bot_uptime,
                    error_count=stats.error_count,
                    created_at=stats.created_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching daily stats: {str(e)}")

    @fastapi_app.get("/api/dailystats/latest", response_model=DailyStatsResponse)
    async def get_latest_dailystats():
        """Get the latest daily statistics."""
        try:
            with rx.session() as session:
                stats = session.query(DailyStatistics).order_by(DailyStatistics.date.desc()).first()
                if not stats:
                    raise HTTPException(status_code=404, detail="No daily stats found")
                
                return DailyStatsResponse(
                    id=stats.id,
                    date=stats.date,
                    total_revenue=stats.total_revenue,
                    total_users=stats.total_users,
                    active_users=stats.active_users,
                    total_transactions=stats.total_transactions,
                    total_gift_cards_sold=stats.total_gift_cards_sold,
                    total_balance=stats.total_balance,
                    bot_uptime=stats.bot_uptime,
                    error_count=stats.error_count,
                    created_at=stats.created_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching latest daily stats: {str(e)}")

    @fastapi_app.put("/api/dailystats/{date}", response_model=DailyStatsResponse)
    async def update_dailystats(date: str, stats: DailyStatsCreate):
        """Update daily statistics by date."""
        try:
            with rx.session() as session:
                existing_stats = session.query(DailyStatistics).filter(DailyStatistics.date == date).first()
                if not existing_stats:
                    raise HTTPException(status_code=404, detail=f"Daily stats for date '{date}' not found")
                
                existing_stats.total_revenue = stats.total_revenue
                existing_stats.total_users = stats.total_users
                existing_stats.active_users = stats.active_users
                existing_stats.total_transactions = stats.total_transactions
                existing_stats.total_gift_cards_sold = stats.total_gift_cards_sold
                existing_stats.total_balance = stats.total_balance
                existing_stats.bot_uptime = stats.bot_uptime
                existing_stats.error_count = stats.error_count
                session.commit()
                session.refresh(existing_stats)
                
                return DailyStatsResponse(
                    id=existing_stats.id,
                    date=existing_stats.date,
                    total_revenue=existing_stats.total_revenue,
                    total_users=existing_stats.total_users,
                    active_users=existing_stats.active_users,
                    total_transactions=existing_stats.total_transactions,
                    total_gift_cards_sold=existing_stats.total_gift_cards_sold,
                    total_balance=existing_stats.total_balance,
                    bot_uptime=existing_stats.bot_uptime,
                    error_count=existing_stats.error_count,
                    created_at=existing_stats.created_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating daily stats: {str(e)}")

    @fastapi_app.delete("/api/dailystats/{date}")
    async def delete_dailystats(date: str):
        """Delete daily statistics by date."""
        try:
            with rx.session() as session:
                stats = session.query(DailyStatistics).filter(DailyStatistics.date == date).first()
                if not stats:
                    raise HTTPException(status_code=404, detail=f"Daily stats for date '{date}' not found")
                
                session.delete(stats)
                session.commit()
                return {"message": f"Daily stats for date '{date}' deleted successfully"}
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting daily stats: {str(e)}")