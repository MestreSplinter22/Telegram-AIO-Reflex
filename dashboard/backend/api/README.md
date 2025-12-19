# Centralized API Structure

This directory contains all API endpoints for the TelegramaIO application.

## Structure

Each API module should follow this pattern:

```python
# Create a folder for your API (e.g., users, products, transactions)
# Inside the folder, create __init__.py with the following structure:

"""Description of your API module."""

from fastapi import FastAPI

def register_your_api_routes(app: FastAPI):
    """Register your API routes."""
    
    @app.get("/api/your-endpoint")
    async def your_endpoint():
        return {"message": "Hello from your API"}
```

## Adding New APIs

1. Create a new folder in `backend/api/` with your API name
2. Create `__init__.py` inside the folder following the pattern above
3. Add the registration function to the main API system in `backend/api/__init__.py`
4. Import and register the routes in `dashboard.py`

## Current APIs

- **healthy**: Health check endpoint (`/api/healthy`)
  - File: `backend/api/healthy/__init__.py`
  - Purpose: Basic API health check and database connectivity test

- **botconfig**: Bot configuration management (`/api/botconfig`)
  - File: `backend/api/botconfig/__init__.py`
  - Purpose:## Current APIs

- **healthy** - Health check endpoint
  - `GET /api/healthy` - Check API and database health

- **botconfig** - CRUD operations for BotConfig table using Reflex ORM
  - `POST /api/botconfig` - Create new configuration
  - `GET /api/botconfig` - List all configurations
  - `GET /api/botconfig/{key}` - Get configuration by key
  - `PUT /api/botconfig/{key}` - Update configuration by key
  - `DELETE /api/botconfig/{key}` - Delete configuration by key

- **users** - CRUD operations for User table using Reflex ORM
  - `POST /api/users` - Create new user
  - `GET /api/users` - List all users
  - `GET /api/users/{telegram_id}` - Get user by telegram_id
  - `PUT /api/users/{telegram_id}` - Update user by telegram_id
  - `DELETE /api/users/{telegram_id}` - Delete user by telegram_id

- **transactions** - CRUD operations for Transaction table using Reflex ORM
  - `POST /api/transactions` - Create new transaction
  - `GET /api/transactions` - List all transactions
  - `GET /api/transactions/{transaction_id}` - Get transaction by ID
  - `GET /api/transactions/user/{user_id}` - Get transactions by user
  - `PUT /api/transactions/{transaction_id}` - Update transaction by ID
  - `DELETE /api/transactions/{transaction_id}` - Delete transaction by ID

- **giftcards** - CRUD operations for GiftCard table using Reflex ORM
  - `POST /api/giftcards` - Create new gift card
  - `GET /api/giftcards` - List all gift cards
  - `GET /api/giftcards/{code}` - Get gift card by code
  - `GET /api/giftcards/category/{category}` - Get gift cards by category
  - `GET /api/giftcards/status/{status}` - Get gift cards by status
  - `PUT /api/giftcards/{code}` - Update gift card by code
  - `DELETE /api/giftcards/{code}` - Delete gift card by code

- **botlogs** - CRUD operations for BotLog table using Reflex ORM
  - `POST /api/botlogs` - Create new bot log
  - `GET /api/botlogs` - List all bot logs
  - `GET /api/botlogs/{log_id}` - Get bot log by ID
  - `GET /api/botlogs/user/{user_id}` - Get bot logs by user
  - `GET /api/botlogs/level/{level}` - Get bot logs by level
  - `DELETE /api/botlogs/{log_id}` - Delete bot log by ID
  - `DELETE /api/botlogs/user/{user_id}` - Delete all bot logs for user

- **dailystats** - CRUD operations for DailyStatistics table using Reflex ORM
  - `POST /api/dailystats` - Create new daily statistics
  - `GET /api/dailystats` - List all daily statistics
  - `GET /api/dailystats/{date}` - Get daily stats by date (YYYY-MM-DD)
  - `GET /api/dailystats/latest` - Get latest daily statistics
  - `PUT /api/dailystats/{date}` - Update daily stats by date
  - `DELETE /api/dailystats/{date}` - Delete daily stats by date