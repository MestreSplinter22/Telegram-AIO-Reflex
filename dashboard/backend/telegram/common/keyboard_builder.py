from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

def create_button(btn_data: dict) -> InlineKeyboardButton:
    """
    Cria um botão baseado no dicionário de configuração.
    Suporta: callback, url, web_app.
    """
    text = btn_data.get("text", "Botão")
    
    if "callback" in btn_data:
        return InlineKeyboardButton(text=text, callback_data=btn_data["callback"])
    
    if "url" in btn_data:
        return InlineKeyboardButton(text=text, url=btn_data["url"])
        
    if "web_app" in btn_data:
        return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=btn_data["web_app"]))

    # Adicione outros tipos aqui se necessário (switch_inline_query, etc)
    return InlineKeyboardButton(text=text, callback_data="noop")

def build_keyboard(rows: list) -> InlineKeyboardMarkup:
    """
    Recebe uma lista de listas (linhas de botões) do JSON e retorna o Markup.
    """
    keyboard = []
    for row in rows:
        keyboard_row = [create_button(btn) for btn in row]
        keyboard.append(keyboard_row)
            
    return InlineKeyboardMarkup(inline_keyboard=keyboard)