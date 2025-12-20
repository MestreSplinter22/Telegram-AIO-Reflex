from aiogram import types
from .keyboard_builder import build_keyboard

async def send_template_message(
    message: types.Message, 
    template: dict, 
    context: dict = None
):
    """
    Envia uma mensagem baseada em um template JSON.
    
    Args:
        message: Objeto Message ou CallbackQuery do aiogram
        template: Dicionário contendo a configuração da mensagem (do JSON)
        context: Dicionário com variáveis para substituir no texto (ex: {name: 'João'})
    """
    # Se for CallbackQuery, pegamos a mensagem original
    if isinstance(message, types.CallbackQuery):
        target = message.message
    else:
        target = message

    # 1. Processar Texto
    text = template.get("text", "")
    if context:
        try:
            text = text.format(**context)
        except KeyError as e:
            text = text # Fallback se faltar variável
            
    # 2. Construir Teclado
    markup = None
    if "buttons" in template:
        markup = build_keyboard(template["buttons"])

    # 3. Enviar (com ou sem imagem)
    image_url = template.get("image_url")
    
    if image_url:
        # Se tem imagem, envia photo (ou edita se possível, mas photo geralmente envia nova)
        # Para fluxos complexos, sugerido deletar a anterior e enviar nova para manter "limpo"
        await target.answer_photo(
            photo=image_url,
            caption=text,
            reply_markup=markup,
            parse_mode="HTML"
        )
    else:
        # Apenas texto
        await target.answer(
            text=text,
            reply_markup=markup,
            parse_mode="HTML",
            disable_web_page_preview=False
        )