import asyncio
from contextlib import asynccontextmanager
from .bot import start_telegram_bot, stop_telegram_bot

# Variável global para armazenar a task do bot
telegram_task = None

@asynccontextmanager
async def telegram_lifespan(app):
    """
    Lifespan manager para integrar o bot do Telegram com Reflex usando aiogram
    """
    global telegram_task
    
    # Inicialização
    print("Iniciando lifespan do Telegram...")
    try:
        # Iniciar o bot do Telegram
        telegram_task = await start_telegram_bot()
        print("Bot do Telegram iniciado no lifespan")
        
        yield  # Reflex app está rodando
        
    except Exception as e:
        print(f"Erro durante inicialização do Telegram: {e}")
        raise
    
    finally:
        # Cleanup
        print("Encerrando lifespan do Telegram...")
        if telegram_task:
            await stop_telegram_bot(telegram_task)
            telegram_task = None
            print("Bot do Telegram encerrado no lifespan")