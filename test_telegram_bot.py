#!/usr/bin/env python3
"""
Script para testar se o bot do Telegram está funcionando corretamente
"""

import asyncio
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard.backend.telegram.bot import is_bot_running
from dashboard.backend.telegram.startup import startup_telegram_bot, shutdown_telegram_bot

async def test_bot():
    """Testa o bot do Telegram"""
    print("=== Testando Bot do Telegram ===")
    
    # Testar status inicial
    print(f"Status inicial do bot: {'Rodando' if is_bot_running() else 'Parado'}")
    
    # Tentar iniciar o bot
    print("Iniciando bot...")
    await startup_telegram_bot()
    
    # Aguardar um momento para o bot iniciar
    await asyncio.sleep(2)
    
    # Verificar status
    print(f"Status após inicialização: {'Rodando' if is_bot_running() else 'Parado'}")
    
    # Testar shutdown
    print("Desligando bot...")
    await shutdown_telegram_bot()
    
    # Verificar status final
    print(f"Status final: {'Rodando' if is_bot_running() else 'Parado'}")
    
    print("=== Teste concluído ===")

if __name__ == "__main__":
    asyncio.run(test_bot())