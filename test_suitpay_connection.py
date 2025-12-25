import requests
import json
import uuid
from datetime import datetime, timedelta

# --- SUAS CREDENCIAIS ---
CLIENT_ID = "dege22_1754575850408" 
CLIENT_SECRET = "1fa82afc16affdae24dc1fd356e41fd59d497b49665a507d564de67a6b6c37a641881a66c2b74a20bf3ca5d29c9b2e72"
BASE_URL = "https://ws.suitpay.app/api/v1/gateway/request-qrcode"

def teste_diagnostico_pix():
    # DADOS DE TESTE (Use dados REAIS seus para testar em produção)
    valor = 2.00  # Tente valor inteiro
    nome = "Seu Nome Completo"
    cpf = "13592187775" # Coloque seu CPF verdadeiro (sem pontos) para testar
    email = "seu.email@exemplo.com"

    # Limpeza do CPF
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    
    # Validação básica
    if len(cpf_limpo) != 11 and len(cpf_limpo) != 14:
        print(f"❌ Erro: CPF/CNPJ parece inválido: {cpf_limpo}")
        return

    request_number = str(uuid.uuid4())
    data_vencimento = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    payload = {
        "requestNumber": request_number,
        "dueDate": data_vencimento,
        "amount": valor,
        "shippingAmount": 0.0,
        "callbackUrl": "https://webhook.site/seu-hash", # Pode deixar fake por enquanto
        "client": {
            "name": nome,
            "document": cpf_limpo,
            "email": email
        }
    }

    headers = {
        'ci': CLIENT_ID,
        'cs': CLIENT_SECRET,
        'Content-Type': 'application/json'
    }

    print("--- DADOS ENVIADOS ---")
    print(json.dumps(payload, indent=2))
    print("----------------------")

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Erro de conexão: {e}")

if __name__ == "__main__":
    teste_diagnostico_pix()