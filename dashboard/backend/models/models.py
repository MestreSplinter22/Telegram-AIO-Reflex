import reflex as rx
from datetime import datetime
from typing import Optional, Dict, Any

class User(rx.Model, table=True):
    telegram_id: str
    username: str
    first_name: str
    last_name: str
    balance: float = 0.0
    total_spent: float = 0.0
    status: str = "active"  # active, suspended, banned
    created_at: datetime = rx.Field(default_factory=datetime.utcnow)
    updated_at: datetime = rx.Field(default_factory=datetime.utcnow)
    last_activity: Optional[datetime] = None
    risk_score: float = 0.0

class Transaction(rx.Model, table=True):
    user_id: str
    type: str  # deposit, purchase, refund, manual_adjustment
    amount: float
    description: str
    status: str = "pending"  # completed, pending, failed, refunded
    timestamp: datetime = rx.Field(default_factory=datetime.utcnow)
    pix_key: Optional[str] = None
    extra_data: Optional[str] = None

class GiftCard(rx.Model, table=True):
    code: str
    category: str
    value: float
    cost_price: float
    selling_price: float
    status: str = "active"  # active, redeemed, expired
    created_at: datetime = rx.Field(default_factory=datetime.utcnow)
    redeemed_by: Optional[str] = None
    redeemed_at: Optional[datetime] = None

class BotLog(rx.Model, table=True):
    level: str  # info, warning, error, debug
    message: str
    timestamp: datetime = rx.Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    extra_data: Optional[str] = None

class BotConfig(rx.Model, table=True):
    key: str
    value: str
    description: Optional[str] = None
    updated_at: datetime = rx.Field(default_factory=datetime.utcnow)

class DailyStatistics(rx.Model, table=True):
    date: str  # YYYY-MM-DD format
    total_revenue: float = 0.0
    total_users: int = 0
    active_users: int = 0
    total_transactions: int = 0
    total_gift_cards_sold: int = 0
    total_balance: float = 0.0
    bot_uptime: float = 0.0
    error_count: int = 0
    created_at: datetime = rx.Field(default_factory=datetime.utcnow)

# Helper function to create all tables
def create_all():
    """Create all database tables using Reflex's built-in functionality."""
    pass