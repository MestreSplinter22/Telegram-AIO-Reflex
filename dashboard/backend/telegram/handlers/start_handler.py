import json
import os
from aiogram import Router, types
from aiogram.filters import Command
from ..common.message_handler import send_template_message

router = Router()

# Função auxiliar para carregar o JSON (pode ir para um utils)
def load_flow(flow_name):
    # Ajuste o caminho conforme sua estrutura
    path = f"dashboard/backend/telegram/flows/{flow_name}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.message(Command("start"))
async def start_command(message: types.Message):
    # 1. Carregar configuração
    flow_data = load_flow("start_flow")
    screen_config = flow_data["welcome_screen"]
    
    # 2. Preparar contexto (dados dinâmicos)
    user_context = {
        "name": message.from_user.full_name,
        "id": message.from_user.id
    }
    
    # 3. Delegar para o sistema common
    await send_template_message(message, screen_config, context=user_context)