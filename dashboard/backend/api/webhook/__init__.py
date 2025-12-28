"""
API Endpoint para Webhook Pix da Efí Bank.
"""

from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import logging
import os
from ...flowbuilder import start_flow

# Configuração de Logs
logger = logging.getLogger(__name__)

# Modelos Pydantic baseados na documentação da Efí
class PixData(BaseModel):
    endToEndId: str
    txid: str
    chave: str
    valor: str
    horario: str
    infoPagador: Optional[str] = None

class WebhookPayload(BaseModel):
    pix: List[PixData]

def register_webhook_routes(app: FastAPI):
    
    # Aceita com ou sem barra no final
    @app.post("/api/webhook/pix")
    @app.post("/api/webhook/pix/")
    async def efi_pix_webhook(request: Request):
        try:
            # Tenta ler o JSON, se não vier nada, usa um dict vazio
            try:
                payload = await request.json()
            except:
                payload = {}

            logger.info(f"🔔 Webhook Recebido: {payload}")
            
            # Se for apenas o teste de validação da Efí (sem a chave 'pix')
            if not payload or "pix" not in payload:
                return {"status": 200, "detail": "Webhook ativo"}

            # Se chegamos aqui, é um Pix real. Processamos:
            from ...flowbuilder import start_flow
            for pix in payload.get("pix", []):
                # O flow_handler cuidará de achar o user pelo txid
                await start_flow(user_id="0", flow_name="pix_received", data=pix)

            return {"status": 200}
            
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {e}")
            # Retornamos 200 mesmo no erro para não quebrar o registro da Efí
            return {"status": 200, "error": str(e)}