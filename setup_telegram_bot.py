#!/usr/bin/env python3
"""
Script auxiliar para configuração do bot do Telegram
"""

import os
import sys
import shutil

def setup_telegram_bot():
    """Configura o bot do Telegram"""
    print("=== Configuração do Bot do Telegram ===")
    
    # Verificar se .env existe
    if not os.path.exists('.env'):
        print("Criando arquivo .env a partir do exemplo...")
        shutil.copy('.env.example', '.env')
        print("✅ Arquivo .env criado!")
    else:
        print("✅ Arquivo .env já existe!")
    
    # Verificar se o token está configurado
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token and token != 'seu_token_aqui':
        print("✅ Token do Telegram já está configurado!")
    else:
        print("⚠️  Token do Telegram não está configurado.")
        print("   1. Abra o arquivo .env")
        print("   2. Substitua 'seu_token_aqui' pelo seu token real")
        print("   3. Ou defina a variável de ambiente: export TELEGRAM_BOT_TOKEN='seu_token'")
    
    print("\n=== Teste rápido ===")
    print("Após configurar o token, você pode:")
    print("1. Iniciar o Reflex: reflex run")
    print("2. Verificar status: curl http://localhost:8000/api/telegram/status")
    print("3. Testar bot: curl http://localhost:8000/api/telegram/test")

if __name__ == "__main__":
    setup_telegram_bot()