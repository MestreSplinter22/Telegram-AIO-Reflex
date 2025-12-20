"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx
from fastapi import FastAPI

# Importar dotenv para carregar variáveis de ambiente
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

from . import styles
from .pages import *
from .backend.models import create_all
from .backend.api import register_all_routes


import asyncio
from contextlib import asynccontextmanager
from .backend.telegram.startup import startup_telegram_bot, shutdown_telegram_bot
from dashboard.pages.flow_builder import flow_builder_page

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan para gerenciar o ciclo de vida do aplicativo"""
    # Bot do Telegram não será inicializado automaticamente
    # Use os endpoints /api/telegram/start e /api/telegram/stop para controle manual
    try:
        yield
    finally:
        # Limpar recursos apenas se o bot estiver rodando
        await shutdown_telegram_bot()

# Criar uma instância FastAPI para o api_transformer
fastapi_app = FastAPI(title="TelegramaIO API", lifespan=lifespan)

# Register all API routes centrally
register_all_routes(fastapi_app)

# Create the app.
app = rx.App(
    theme=rx.theme(appearance="dark"),
    stylesheets=["/style.css"],
    api_transformer=fastapi_app,
)

# Create all database tables when the app starts
create_all()

app.add_page(
    rx.center(
        rx.text("Tailwind & Reflex!"),
        class_name="bg-background w-full h-[100vh]",
    ),
    "/teste",
)
