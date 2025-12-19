from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from dashboard.backend.models.models import User
from dashboard.backend.database import get_db_session
import logging
from datetime import datetime
import reflex as rx
import asyncio
from typing import Optional

router = Router()
logger = logging.getLogger(__name__)

def _get_or_create_user_sync(telegram_id: int, username: Optional[str] = None, full_name: Optional[str] = None) -> dict:
    """Get or create a user and return as dictionary to avoid session issues."""
    
    with rx.session() as session:
        # Find existing user - usando approach mais simples que funciona com Reflex
        try:
            # Try to find user
            result = None
            for user in session.query(User).all():
                if user.telegram_id == str(telegram_id):
                    result = user
                    break
        except Exception as e:
            logger.error(f"Error querying users: {e}")
            result = None
        
        if not result:
            # Split full_name into first_name and last_name
            if full_name:
                name_parts = full_name.strip().split(' ', 1)
                first_name = name_parts[0] if name_parts else ""
                last_name = name_parts[1] if len(name_parts) > 1 else ""
            else:
                first_name = ""
                last_name = ""
            
            user = User(
                telegram_id=str(telegram_id),
                username=username or "",
                first_name=first_name,
                last_name=last_name,
                balance=0.0,
                total_spent=0.0,
                status="active",
                risk_score=0.0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"New user created: {telegram_id}")
            
            # Return as dictionary to avoid detached instance
            return {
                'telegram_id': user.telegram_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'balance': user.balance,
                'total_spent': user.total_spent,
                'status': user.status,
                'risk_score': user.risk_score,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
        else:
            changes = False
            # Update username if changed
            if username and result.username != username:
                result.username = username
                changes = True
            
            # Update first_name and last_name if full_name provided
            if full_name:
                name_parts = full_name.strip().split(' ', 1)
                first_name = name_parts[0] if name_parts else ""
                last_name = name_parts[1] if len(name_parts) > 1 else ""
                
                # Normalize DB values to empty string for comparison if None
                current_first_name = result.first_name or ""
                current_last_name = result.last_name or ""
                
                if current_first_name != first_name:
                    result.first_name = first_name
                    changes = True
                if current_last_name != last_name:
                    result.last_name = last_name
                    changes = True
            
            if changes:
                result.updated_at = datetime.utcnow()
                session.add(result)
                session.commit()
                session.refresh(result)
            
            # Return as dictionary to avoid detached instance
            return {
                'telegram_id': result.telegram_id,
                'username': result.username,
                'first_name': result.first_name,
                'last_name': result.last_name,
                'balance': result.balance,
                'total_spent': result.total_spent,
                'status': result.status,
                'risk_score': result.risk_score,
                'created_at': result.created_at,
                'updated_at': result.updated_at
            }

async def get_or_create_user(telegram_id: int, username: Optional[str] = None, full_name: Optional[str] = None) -> dict:
    return await asyncio.to_thread(_get_or_create_user_sync, telegram_id, username, full_name)

@router.message(Command("start"))
async def start_command(message: types.Message):
    if not message.from_user:
        return
    
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    
    user = await get_or_create_user(telegram_id, username, full_name)
    
    # Format the welcome message
    welcome_text = (
        f"<a href='https://i.ibb.co/rmn2VqT/akst.jpg'>👋</a> Olá <b>{full_name or 'Usuário'}</b>!\n"
        f"📢 <a href='https://t.me/akatsukicentral'>Grupo</a>\n"
        f"🧾 Seu perfil:\n"
        f"  ├👤 <b>ID:</b> <code>{telegram_id}</code>\n"
        f"  └💸 <b>Saldo:</b> R$ <b>{user['balance']:.2f}</b>\n\n"
        f"🟢 <b>BÔNUS DE RECARGA ATIVO</b>\n"
        f"💸 <b>RECEBE 100% DE BÔNUS</b>\n\n"
        f"🔽 <b>VALOR MÍNIMO: R$ 50</b>"
    )
    
    # Create inline keyboard buttons
    keyboard = [
        [InlineKeyboardButton(text="AKATSUKI SHOPPING", callback_data="shopping")],
        [InlineKeyboardButton(text="ADICIONAR SALDO", callback_data="add_balance")],
        [InlineKeyboardButton(text="BOT DE PUXADA", url="https://t.me/buscasfacilbot?start=1665512795")],
        [
            InlineKeyboardButton(text="PERFIL", callback_data="profile"),
            InlineKeyboardButton(text="AJUDA", url="https://t.me/ItachiADM")
        ]
    ]
    
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await message.answer(
        text=welcome_text,
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=False
    )
    
    logger.info(f"Start command executed for user: {telegram_id}")