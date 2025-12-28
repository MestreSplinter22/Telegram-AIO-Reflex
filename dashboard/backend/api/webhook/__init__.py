# dashboard/backend/api/webhook.py

from fastapi import APIRouter, Request, HTTPException
import logging
import reflex as rx
import json

# Importações para atualizar o Banco de Dados
from dashboard.backend.models.models import Transaction, User
from dashboard.backend.telegram.bot import bot

logger = logging.getLogger(__name__)

def register_webhook_routes(app):
    router = APIRouter(tags=["Webhook"])

    @router.api_route("/webhook", methods=["POST", "GET", "PUT", "DELETE"])
    async def universal_webhook(request: Request):
        try:
            method = request.method
            # Tenta ler o corpo
            try:
                payload = await request.json()
                content_type = "json"
            except Exception:
                body_bytes = await request.body()
                payload = body_bytes.decode("utf-8", errors="replace")
                content_type = "raw/text"

            logger.info(f"--- WEBHOOK RECEBIDO ({method}) ---")
            logger.info(f"Payload: {payload}")

            if isinstance(payload, dict):
                # 1. Validação de Cadastro (URL)
                if "webhookUrl" in payload:
                    return {"status": 200}
                
                # 2. NOVO: Validação de Teste da Efí (O que apareceu no seu log)
                if payload.get("evento") == "teste_webhook":
                    logger.info("✅ Evento de Teste da Efí recebido com sucesso!")
                    return {"status": 200}

                # 3. Pagamento Real (Pix)
                if "pix" in payload:
                    await process_efi_payment(payload)
                    return {"status": 200}

            return {"status": "received"}

        except Exception as e:
            logger.error(f"Erro no webhook: {e}")
            # A Efí tenta reenviar se der erro 500, então cuidado
            raise HTTPException(status_code=500, detail="Internal Error")

    app.include_router(router, prefix="/api")

# --- FUNÇÃO AUXILIAR PARA PROCESSAR O PAGAMENTO DA EFÍ ---
async def process_efi_payment(data: dict):
    """
    Processa a lista de PIX recebidos no JSON da Efí.
    Formato esperado: { "pix": [ { "txid": "...", "valor": "...", "status": "CONCLUIDA" } ] }
    """
    pix_list = data.get("pix", [])
    
    with rx.session() as session:
        for item in pix_list:
            txid = item.get("txid")
            valor = item.get("valor") # Vem como string "10.00"
            
            print(f"💰 Processando PIX Efí TXID: {txid} - Valor: {valor}")

            # Busca a transação pelo TXID salvo no extra_data
            # O extra_data é JSON, então usamos busca textual simples ou filtro específico
            # No PostgreSQL/SQLAlchemy, LIKE é o mais simples se não usar JSONB
            
            # Busca todas as pendentes para filtrar no Python (mais seguro com JSON string)
            pending_txns = session.query(Transaction).filter(
                Transaction.status == "pending"
            ).all()

            target_txn = None
            for txn in pending_txns:
                if txn.extra_data and txid in txn.extra_data:
                    target_txn = txn
                    break
            
            if not target_txn:
                print(f"⚠️ Transação não encontrada para TXID: {txid}")
                continue

            # Atualiza Transação
            target_txn.status = "completed"
            session.add(target_txn)

            # Credita Saldo
            user = session.query(User).filter(User.id == int(target_txn.user_id)).first()
            if user:
                amount_float = float(valor)
                user.balance += amount_float
                user.total_spent += amount_float
                session.add(user)

                # Notifica Telegram
                try:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"✅ <b>Pix Efí Confirmado!</b>\n\n💰 + R$ {amount_float:.2f}",
                        parse_mode="HTML"
                    )
                except Exception as e:
                    print(f"Erro notificação Telegram: {e}")

            session.commit()
            print(f"✅ Transação {target_txn.id} liquidada (Efí).")