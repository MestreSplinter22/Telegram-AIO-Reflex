"""Centralized API imports for all endpoints."""

from .healthy import register_healthy_routes
from .botconfig import register_botconfig_routes
from .users import register_user_routes
from .transactions import register_transactions_routes
from .giftcards import register_giftcards_routes
from .botlogs import register_botlogs_routes
from .dailystats import register_dailystats_routes
from ..telegram.routes import register_telegram_routes

# --- ADICIONE ESTA IMPORTAÇÃO ---
from .gateways.routes import register_payment_routes 

API_REGISTRARS = [
    register_healthy_routes,
    register_botconfig_routes,
    register_user_routes,
    register_transactions_routes,
    register_giftcards_routes,
    register_botlogs_routes,
    register_dailystats_routes,
    register_telegram_routes,
    # --- REGISTRE AQUI ---
    register_payment_routes, 
]

def register_all_routes(app):
    """Register all API routes from all modules."""
    for registrar in API_REGISTRARS:
        registrar(app)