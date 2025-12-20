# dashboard/backend/telegram/handlers/start_handler.py
import json
from aiogram import Router, types , F
from aiogram.filters import Command
from ..common.message_handler import send_template_message

router = Router()

def load_flow_data():
    path = "dashboard/backend/telegram/flows/start_flow.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.message(Command("start"))
async def start_command(message: types.Message):
    data = load_flow_data()
    
    # Pega o nome da tela inicial definido no JSON
    initial_key = data.get("initial_screen", "language_selection")
    screen_config = data["screens"][initial_key]
    
    await send_template_message(message, screen_config, context={"name": message.from_user.first_name})

@router.message(F.video)
async def capture_video_id(message: types.Message):
    file_id = message.video.file_id
    await message.answer(
        f"📹 <b>ID do Vídeo para seu JSON:</b>\n\n<code>{file_id}</code>", 
        parse_mode="HTML"
    )