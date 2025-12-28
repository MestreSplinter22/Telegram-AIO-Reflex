from efipay import EfiPay
import os
from dotenv import load_dotenv

load_dotenv()

# Caminho exato que você configurou
CERT_PATH = "dashboard/backend/api/gateways/efi/credencial/certificado.pem"

credentials = {
    'client_id': "Client_Id_497c00249fd13a6b4058e67cfc751d9ec6100775",
    'client_secret': "Client_Secret_cbd25e7acd2c42a6ef6745736a649e1b8743909e",
    'sandbox': False, # Mude para True se for homologação
    'certificate': CERT_PATH
}

efi = EfiPay(credentials)

def ativar():
    # 1. Sua chave PIX cadastrada na Efí
    params = {'chave': '5726ec81-0287-4657-b68d-90f6d9629b2e'} 
    
    # 2. A URL do seu servidor (precisa ser HTTPS)
    # Importante: O sufixo /pix é adicionado pela Efí, então a URL base é:
    body = {'webhookUrl': 'https://api.promosdiarias.shop/api/webhook/pix'}

    # 3. Cabeçalho para Skip-mTLS (Para facilitar a conexão no seu servidor)
    headers = {'x-skip-mtls-checking': 'true'}

    try:
        response = efi.pix_config_webhook(params=params, body=body, headers=headers)
        print("✅ Sucesso ao registrar!")
        print(response)
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    ativar()