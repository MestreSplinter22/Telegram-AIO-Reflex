"""Base data models for the dashboard."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    """User model for gift card system."""
    id: str
    telegram_id: str
    username: str
    name: str
    email: str
    balance: float
    total_spent: float
    total_orders: int
    created_at: datetime
    last_activity: datetime
    status: str  # active, suspended, banned
    risk_score: float  # 0-100 for fraud detection


class Transaction(BaseModel):
    """Transaction model for PIX and gift card purchases."""
    id: str
    user_id: str
    type: str  # deposit, purchase, refund, manual_adjustment
    amount: float
    status: str  # pending, completed, failed, refunded
    description: str
    pix_key: Optional[str] = None
    pix_transaction_id: Optional[str] = None
    gift_card_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    metadata: dict = {}


class GiftCard(BaseModel):
    """Gift card product model."""
    id: str
    name: str
    category: str
    value: float
    cost_price: float
    selling_price: float
    profit_margin: float
    stock: int
    sold_count: int
    status: str  # active, inactive, discontinued
    created_at: datetime
    image_url: Optional[str] = None


class BotMetrics(BaseModel):
    """Bot performance metrics."""
    id: str
    date: datetime
    active_users: int
    total_messages: int
    commands_executed: int
    response_time_avg: float
    uptime_percentage: float
    errors_count: int