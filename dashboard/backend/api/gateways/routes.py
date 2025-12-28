# dashboard/backend/api/gateways/routes.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import reflex as rx
import uuid
import json
import hashlib

# Imports do Sistema
from dashboard.backend.models.models import GatewayConfig, Transaction, User
from dashboard.backend.gateways.efi_service import EfiPixService
from dashboard.backend.gateways.suitpay_service import SuitPayService
from dashboard.backend.telegram.bot import bot

router = APIRouter(prefix="/api/payment", tags=["payment"])

# --- MODELOS DE DADOS ---
class PaymentRequest(BaseModel):
    user_telegram_id: str
    amount: float
    gateway_name: str = "suitpay" # Define qual gateway usar

class PaymentResponse(BaseModel):
    txid: str
    pix_copia_cola: str
    qrcode_base64: str
    status: str

# --- ROTA DE CRIAÇÃO DE PIX ---
@router.post("/create", response_model=PaymentResponse)
async def create_payment(data: PaymentRequest):
    """
    Cria uma cobrança PIX imediata na Gateway selecionada (Efí ou SuitPay).
    """
    with rx.session() as session:
        # 1. Buscar Gateway Ativo
        gateway = session.query(GatewayConfig).filter(
            GatewayConfig.name == data.gateway_name,
            GatewayConfig.is_active == True
        ).first()
        
        if not gateway:
            # Fallback: Tenta achar a primeira ativa se a solicitada falhar
            gateway = session.query(GatewayConfig).filter(GatewayConfig.is_active == True).first()
            if not gateway:
                raise HTTPException(status_code=404, detail=f"Nenhuma gateway ativa configurada.")

        # 2. Buscar Usuário
        user = session.query(User).filter(User.telegram_id == data.user_telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # 3. Gerar ID Único da Transação
        txid = uuid.uuid4().hex
        
        # Dados do Pagador (Padrão ou do User)
        # Em produção, você deve pegar user.cpf e user.email reais
        cpf = "00000000000" 
        email = "cliente@email.com"
        nome = f"{user.first_name} {user.last_name}"

        pix_result = {}

        try:
            # --- LÓGICA DE SELEÇÃO DE GATEWAY ---
            if gateway.name == "efi_bank":
                service = EfiPixService(gateway)
                # A Efí exige CPF válido em Produção, cuidado com dados fake
                efi_data = service.create_immediate_charge(
                    txid=txid,
                    cpf="12345678909", # Use CPF de teste para Homologação
                    nome=nome,
                    valor=f"{data.amount:.2f}"
                )
                # Normaliza retorno da Efí
                pix_result = {
                    "pix_copia_cola": efi_data.get("qrcode") or efi_data.get("pixCopiaECola"),
                    "qrcode_base64": efi_data.get("imagemQrcode"),
                    "external_id": txid
                }

            elif gateway.name == "suitpay":
                service = SuitPayService(gateway)
                suit_data = service.create_pix_payment(
                    txid=txid, 
                    cpf=cpf, 
                    nome=nome, 
                    email=email, 
                    valor=data.amount
                )
                # Normaliza retorno da SuitPay
                pix_result = {
                    "pix_copia_cola": suit_data.get("pix_copia_cola"),
                    "qrcode_base64": suit_data.get("qrcode_base64"),
                    "external_id": suit_data.get("txid")
                }

            else:
                raise HTTPException(status_code=400, detail="Gateway não suportada")

            # 4. Salvar Transação no Banco
            new_txn = Transaction(
                user_id=str(user.id),
                type="deposit",
                amount=data.amount,
                description=f"Recarga via {gateway.name}",
                status="pending",
                extra_data=json.dumps({
                    "txid": txid, 
                    "gateway_id": gateway.id, 
                    "external_id": pix_result.get("external_id")
                })
            )
            session.add(new_txn)
            session.commit()

            return {
                "txid": txid,
                "pix_copia_cola": pix_result["pix_copia_cola"],
                "qrcode_base64": pix_result["qrcode_base64"],
                "status": "pending"
            }

        except Exception as e:
            print(f"Erro ao criar pagamento ({gateway.name}): {e}")
            raise HTTPException(status_code=500, detail=str(e))

# --- WEBHOOK SUITPAY ---
@router.post("/webhook/suitpay")
async def suitpay_webhook(request: Request):
    """
    Recebe notificação da SuitPay e confirma pagamento.
    """
    try:
        data = await request.json()
        print(f"🔔 Webhook SuitPay Recebido: {data}")
    except:
        return {"status": "error", "msg": "Invalid JSON"}

    # Validação simples de status
    if data.get("statusTransaction") != "PAID_OUT":
        return {"status": "ignored", "reason": "Not PAID_OUT"}

    request_number = data.get("requestNumber")
    
    with rx.session() as session:
        # Busca transação pendente compatível
        txn = None
        
        # Filtra transações pendentes para otimizar
        txns = session.query(Transaction).filter(Transaction.status == "pending").all()
        
        for t in txns:
            # Verifica se o ID da requisição está nos metadados
            if t.extra_data and (request_number in t.extra_data):
                txn = t
                break
        
        if txn:
            # Valida valor (evita fraudes de pagar R$ 0,01 para recarga de R$ 100)
            valor_pago = float(data.get("value", 0))
            if abs(txn.amount - valor_pago) > 0.05:
                 print(f"❌ Fraude Detectada: Valor esperado {txn.amount}, pago {valor_pago}")
                 return {"status": "error", "msg": "Value mismatch"}

            # Confirma Pagamento
            txn.status = "completed"
            session.add(txn)
            
            # Credita Saldo ao Usuário
            user = session.query(User).filter(User.id == int(txn.user_id)).first()
            if user:
                user.balance += txn.amount
                user.total_spent += txn.amount # Opcional: ajustar lógica contábil
                session.add(user)
                
                # Notifica via Bot
                try:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"✅ <b>Pagamento Confirmado!</b>\n\n💰 Crédito de R$ {txn.amount:.2f} adicionado à sua conta.",
                        parse_mode="HTML"
                    )
                except Exception as e:
                    print(f"Erro ao notificar Telegram: {e}")
            
            session.commit()
            print(f"✅ Transação {txn.id} liquidada com sucesso.")
            return {"response": "OK"}
            
    print(f"⚠️ Transação não encontrada para requestNumber: {request_number}")
    return {"status": "not_found"}

@router.get("/setup-efi-webhook")
async def setup_efi():
    with rx.session() as session:
        gateway = session.query(GatewayConfig).filter(GatewayConfig.name == "efi_bank").first()
        if not gateway:
            return {"error": "Gateway Efí não encontrada no banco"}
        
        service = EfiPixService(gateway)
        # IMPORTANTE: Substitua pela sua URL pública real (ngrok ou produção)
        # Não use localhost aqui
        minha_url = "https://csavy-2804-3a88-ffff-d800-216-3eff-fe8f-c35.a.free.pinggy.link/api/webhook"
        
        try:
            res = service.config_webhook(minha_url)
            return res
        except Exception as e:
            return {"error": str(e)}

# --- WEBHOOK EFI (MANTIDO) ---
@router.post("/webhook/efi")
async def efi_webhook(request: Request):
    # (Mantendo o endpoint para caso você use Efí no futuro)
    # ... código do webhook da Efí se necessário ...
    return {"status": "ok"}

# --- FUNÇÃO DE REGISTRO (ESSA ERA A PEÇA QUE FALTAVA) ---
def register_payment_routes(app):
    app.include_router(router)