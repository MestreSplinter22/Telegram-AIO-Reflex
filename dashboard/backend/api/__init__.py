"""Centralized API imports for all endpoints."""

# This file ensures all API modules are imported and available
# Each API module should provide a register_*_routes function

# Import registration functions
from .healthy import register_healthy_routes
from .botconfig import register_botconfig_routes
from .users import register_user_routes
from .transactions import register_transactions_routes
from .giftcards import register_giftcards_routes
from .botlogs import register_botlogs_routes
from .dailystats import register_dailystats_routes
from ..telegram.routes import register_telegram_routes

# List of all available registration functions
# Add new registration functions here as APIs are created
API_REGISTRARS = [
    register_healthy_routes,
    register_botconfig_routes,
    register_user_routes,
    register_transactions_routes,
    register_giftcards_routes,
    register_botlogs_routes,
    register_dailystats_routes,
    register_telegram_routes,
]

def register_all_routes(app):
    """Register all API routes from all modules."""
    for registrar in API_REGISTRARS:
        registrar(app)