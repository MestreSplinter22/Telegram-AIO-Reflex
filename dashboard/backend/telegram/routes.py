from fastapi import APIRouter, HTTPException, FastAPI
import logging
from .bot import start_telegram_bot, stop_telegram_bot, is_bot_running, get_bot_info

router = APIRouter(prefix="/api/telegram", tags=["telegram"])
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_bot_status():
    """Retorna o status detalhado do bot do Telegram"""
    info = get_bot_info()
    return {
        "running": info["running"],
        "token_configured": info["token_configured"],
        "token_env_var": info["token_env_var"],
        "application_instance": info["application_instance"],
        "message": "Bot do Telegram está funcionando" if info["running"] else "Bot do Telegram não está rodando",
        "details": info
    }

@router.post("/start")
async def start_bot():
    """Inicia o bot do Telegram manualmente"""
    try:
        result = await start_telegram_bot()
        if result:
            return {"message": "Bot do Telegram iniciado com sucesso!", "status": "running"}
        else:
            raise HTTPException(status_code=500, detail="Falha ao iniciar o bot do Telegram")
    except Exception as e:
        logger.error(f"Erro ao iniciar bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_bot():
    """Para o bot do Telegram"""
    try:
        result = await stop_telegram_bot()
        if result:
            return {"message": "Bot do Telegram parado com sucesso!", "status": "stopped"}
        else:
            raise HTTPException(status_code=500, detail="Falha ao parar o bot do Telegram")
    except Exception as e:
        logger.error(f"Erro ao parar bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test_bot():
    """Endpoint para testar se o bot está respondendo"""
    info = get_bot_info()
    return {
        "message": "Bot do Telegram integrado com aiogram", 
        "endpoint": "/api/telegram",
        "bot_running": info["running"],
        "token_status": "configured" if info["token_configured"] else "not_configured"
    }

def register_telegram_routes(app: FastAPI):
    """Registra as rotas do Telegram no FastAPI"""
    app.include_router(router)