import json
import asyncio
from aiogram import Router, F, types
from ..common.message_handler import send_template_message

router = Router()

def load_flow_screens():
    path = "dashboard/backend/telegram/flows/start_flow.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["screens"]

@router.callback_query(F.data.startswith("goto_"))
async def navigation_handler(callback: types.CallbackQuery):
    target_screen_key = callback.data.replace("goto_", "")
    screens = load_flow_screens()
    
    if target_screen_key in screens:
        screen_data = screens[target_screen_key]
        user_context = {
            "name": callback.from_user.first_name,
            "id": callback.from_user.id
        }
        
        try:
            # 1. Apaga a mensagem anterior (o menu que foi clicado)
            # Isso mantém o chat limpo antes de mandar as novas mensagens
            await callback.message.delete()
        except Exception:
            pass # Se não der pra apagar (msg muito antiga), segue o baile

        # 2. Verifica se é uma LISTA de mensagens ou uma ÚNICA mensagem
        if isinstance(screen_data, list):
            # É uma sequência (ex: Vídeo -> Texto com Botões)
            for part in screen_data:
                await send_template_message(
                    message=callback.message, # Usa o objeto message original para saber onde enviar
                    template=part,
                    context=user_context
                )
                # Pequena pausa para garantir a ordem de envio no Telegram
                await asyncio.sleep(0.3)
        else:
            # É uma mensagem única (padrão antigo)
            await send_template_message(
                message=callback.message,
                template=screen_data,
                context=user_context
            )
            
    else:
        await callback.answer("Opção indisponível.", show_alert=True)
    
    await callback.answer()