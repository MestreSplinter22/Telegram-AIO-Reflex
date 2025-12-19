import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from .startup import startup_telegram_bot, shutdown_telegram_bot

# Carregar variáveis de ambiente do arquivo .env
dotenv_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))) / '.env'
load_dotenv(dotenv_path)

logger = logging.getLogger(__name__)

# Inicialização automática removida - usar endpoints manuais
__all__ = ['startup_telegram_bot', 'shutdown_telegram_bot']