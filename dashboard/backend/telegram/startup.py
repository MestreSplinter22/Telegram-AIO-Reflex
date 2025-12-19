import asyncio
import logging
from typing import Optional
from .bot import start_telegram_bot, stop_telegram_bot

logger = logging.getLogger(__name__)
telegram_task: Optional[asyncio.Task] = None

async def startup_telegram_bot():
    """Inicia o bot do Telegram quando o Reflex iniciar"""
    global telegram_task
    
    try:
        logger.info("Iniciando bot do Telegram...")
        telegram_task = await start_telegram_bot()
        logger.info("Bot do Telegram iniciado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao iniciar bot do Telegram: {e}")
        return False

async def shutdown_telegram_bot():
    """Para o bot do Telegram quando o Reflex encerrar"""
    global telegram_task
    
    try:
        if telegram_task:
            logger.info("Encerrando bot do Telegram...")
            await stop_telegram_bot(telegram_task)
            telegram_task = None
            logger.info("Bot do Telegram encerrado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao encerrar bot do Telegram: {e}")