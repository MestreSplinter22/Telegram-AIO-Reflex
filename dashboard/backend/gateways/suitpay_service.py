# dashboard/backend/gateways/suitpay_service.py

import requests
import json
from datetime import datetime, timedelta
from dashboard.backend.models.models import GatewayConfig

class SuitPayService:
    def __init__(self, config: GatewayConfig):
        self.config = config
        self.creds = config.credentials
        self.base_url = self.creds.get("base_url", "https://sandbox.ws.suitpay.app")
        
        # Garante que não há espaços em branco nas chaves
        self.ci = self.creds.get("client_id", "").strip()
        self.cs = self.creds.get("client_secret", "").strip()

    def create_pix_payment(self, txid: str, cpf: str, nome: str, email: str, valor: float):
        """
        Gera um PIX na SuitPay.
        Endpoint: /api/v1/gateway/request-qrcode
        """
        url = f"{self.base_url}/api/v1/gateway/request-qrcode"
        
        # --- CORREÇÃO DO ERRO 403 ---
        # Adicionamos 'User-Agent' para evitar bloqueio de WAF (Firewall)
        headers = {
            'ci': self.ci,
            'cs': self.cs,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Data de vencimento (1 dia)
        due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Limpeza do CPF (apenas números)
        cpf_clean = "".join(filter(str.isdigit, cpf))

        payload = {
            "requestNumber": txid,
            "dueDate": due_date,
            "amount": float(valor),
            "client": {
                "name": nome,
                "document": cpf_clean,
                "email": email
            },
            "callbackUrl": f"https://webhook.site/seu-teste" # Em produção, use sua URL real
        }

        try:
            print(f"📤 Enviando Request SuitPay para: {url}")
            # print(f"Headers: {headers}") # Descomente para debug (Cuidado com logs de produção)
            
            response = requests.post(url, headers=headers, json=payload)
            
            # Se der erro 403/400, tenta mostrar o corpo da resposta para entender o motivo
            if response.status_code != 200:
                print(f"❌ Erro SuitPay {response.status_code}: {response.text}")
                
            response.raise_for_status()
            
            data = response.json()
            
            # Verifica sucesso baseado na resposta da SuitPay
            if data.get("response") == "OK" or "paymentCode" in data:
                return {
                    "txid": data.get("idTransaction") or txid,
                    "pix_copia_cola": data.get("paymentCode"),
                    "qrcode_base64": data.get("paymentCodeBase64")
                }
            else:
                raise Exception(f"Erro na resposta da API: {data}")

        except Exception as e:
            print(f"⚠️ Exceção SuitPay: {str(e)}")
            raise e