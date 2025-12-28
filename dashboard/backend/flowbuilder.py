import logging
import reflex as rx
from datetime import datetime
from .telegram.bot import bot
from .models.models import User, Transaction

logger = logging.getLogger(__name__)

async def start_flow(user_id: str, flow_name: str, data: dict):
    """
    Inicia um fluxo específico. Compatível com a assinatura solicitada.
    """
    if flow_name == "pix_received":
        await flow_handler(user_id, data)

async def flow_handler(user_id: str, data: dict):
    """
    Manipula a lógica de recebimento do Pix:
    1. Atualiza status da transação
    2. Adiciona saldo ao usuário
    3. Envia mensagem no Telegram
    """
    txid = data.get("txid")
    amount = float(data.get("valor", 0.0))
    end_to_end_id = data.get("endToEndId")

    logger.info(f"Iniciando flow de Pix para User {user_id} - TXID {txid}")

    try:
        with rx.session() as session:
            # 1. Buscar e Atualizar a Transação
            # Assumindo que o ID da transação ou extra_data guarda o txid
            transaction = session.query(Transaction).filter(
                (Transaction.extra_data == txid) | (Transaction.id == txid)
            ).first()

            if not transaction:
                logger.error(f"Transação não encontrada para TXID: {txid}")
                return

            if transaction.status == "completed":
                logger.info("Transação já processada anteriormente.")
                return

            transaction.status = "completed"
            transaction.updated_at = datetime.utcnow()
            
            # 2. Atualizar Saldo do Usuário
            user = session.query(User).filter(User.telegram_id == str(user_id)).first()
            if user:
                user.balance += amount
                user.total_spent += amount # Ajuste conforme sua lógica de 'spent' vs 'deposit'
                session.add(user)
                
                # Notificar via Telegram (aiogram)
                try:
                    await bot.send_message(
                        chat_id=int(user.telegram_id),
                        text=(
                            f"✅ <b>Pagamento Confirmado!</b>\n\n"
                            f"💵 Valor: R$ {amount:.2f}\n"
                            f"🆔 TXID: <code>{txid}</code>\n\n"
                            f"Seu saldo foi atualizado."
                        )
                    )
                except Exception as e:
                    logger.error(f"Erro ao enviar mensagem Telegram: {e}")

            session.add(transaction)
            session.commit()
            logger.info(f"Flow finalizado com sucesso para TXID {txid}")

    except Exception as e:
        logger.error(f"Erro crítico no flow_handler: {e}")