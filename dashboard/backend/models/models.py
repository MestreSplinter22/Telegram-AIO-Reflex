# dashboard/backend/models/models.py

import reflex as rx
import sqlmodel
from sqlmodel import Field
from sqlalchemy import Column, JSON
from datetime import datetime
from typing import Optional, Dict, Any

class User(sqlmodel.SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: str
    username: str
    first_name: str
    last_name: str
    balance: float = 0.0
    total_spent: float = 0.0
    status: str = "active"  # active, suspended, banned
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: Optional[datetime] = None
    risk_score: float = 0.0

class Transaction(sqlmodel.SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    type: str  # deposit, purchase, refund, manual_adjustment
    amount: float
    description: str
    status: str = "pending"  # completed, pending, failed, refunded
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    pix_key: Optional[str] = None
    extra_data: Optional[str] = None

class GiftCard(sqlmodel.SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    category: str
    value: float
    cost_price: float
    selling_price: float
    status: str = "active"  # active, redeemed, expired
    created_at: datetime = Field(default_factory=datetime.utcnow)
    redeemed_by: Optional[str] = None
    redeemed_at: Optional[datetime] = None

class BotLog(sqlmodel.SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: str  # info, warning, error, debug
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    extra_data: Optional[str] = None

class BotConfig(sqlmodel.SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    value: str
    description: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DailyStatistics(sqlmodel.SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str  # YYYY-MM-DD format
    total_revenue: float = 0.0
    total_users: int = 0
    active_users: int = 0
    total_transactions: int = 0
    total_gift_cards_sold: int = 0
    total_balance: float = 0.0
    bot_uptime: float = 0.0
    error_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GatewayConfig(rx.Model, table=True):
    name: str = Field(index=True)  # ex: "efi_bank", "mercadopago"
    is_active: bool = False
    is_sandbox: bool = True  # True = Homologação, False = Produção
    
    # Credenciais armazenadas em JSON para flexibilidade
    # Ex: {"client_id": "...", "client_secret": "...", "certificate": "caminho/arquivo.p12"}
    credentials: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    
    # Configurações operacionais
    # Ex: {"min_deposit": 50.00, "webhook_url": "https://seu-app.com/api/webhook/efi"}
    config: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Helper function to create all tables
def create_all():
    """Create all database tables using Reflex's built-in functionality."""
    # Reflex gerencia isso automaticamente, mas mantemos a função para compatibilidade se necessário
    pass