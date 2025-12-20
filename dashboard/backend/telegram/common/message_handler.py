from aiogram import types
from .keyboard_builder import build_keyboard

async def send_template_message(
    message: types.Message, 
    template: dict, 
    context: dict = None
):
    """
    Envia uma mensagem (Texto, Foto ou Vídeo) baseada no JSON.
    """
    # Se for CallbackQuery, pegamos a mensagem original
    target = message.message if isinstance(message, types.CallbackQuery) else message

    # 1. Processar Texto
    text = template.get("text", "")
    if context:
        try:
            text = text.format(**context)
        except KeyError:
            pass # Ignora se faltar variável
            
    # 2. Construir Teclado
    markup = None
    if "buttons" in template:
        markup = build_keyboard(template["buttons"])

    # 3. Verificar Mídia (Vídeo ou Imagem)
    video_url = template.get("video_url")
    image_url = template.get("image_url")
    
    # --- CENÁRIO 1: VÍDEO ---
    if video_url:
        await target.answer_video(
            video=video_url,
            caption=text,
            reply_markup=markup,
            parse_mode="HTML"
        )

    # --- CENÁRIO 2: FOTO ---
    elif image_url:
        await target.answer_photo(
            photo=image_url,
            caption=text,
            reply_markup=markup,
            parse_mode="HTML"
        )

    # --- CENÁRIO 3: APENAS TEXTO ---
    else:
        # Se você quiser usar o truque do link escondido (badge de imagem)
        # você pode colocar o <a href> no texto do JSON, mas o answer_photo acima é mais seguro.
        await target.answer(
            text=text,
            reply_markup=markup,
            parse_mode="HTML",
            disable_web_page_preview=False 
        )