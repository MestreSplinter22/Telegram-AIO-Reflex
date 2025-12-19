import asyncio
import logging
from reflex import event
from .startup import startup_telegram_bot, shutdown_telegram_bot

logger = logging.getLogger(__name__)

@event
async def on_reflex_startup():
    """Evento executado quando o Reflex inicia"""
    logger.info("Reflex iniciando - iniciando bot do Telegram com aiogram...")
    await startup_telegram_bot()

@event
async def on_reflex_shutdown():
    """Evento executado quando o Reflex encerra"""
    logger.info("Reflex encerrando - parando bot do Telegram com aiogram...")
    await shutdown_telegram_bot()