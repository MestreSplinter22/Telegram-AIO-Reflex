# init_suitpay.py
import reflex as rx
from sqlmodel import select
from dashboard.backend.models.models import GatewayConfig

def init_suitpay_config():
    # Credenciais fornecidas
    CLIENT_ID = "dege22_1754575850408"
    CLIENT_SECRET = "30cc19db6b9a41a48b9fa0566308d1ad9db6845c2f702072293bb4a107ea11c23bdfa0b3660f49cbab88e021f028c979"
    
    # URL de Sandbox conforme documentação
    BASE_URL = "https://sandbox.ws.suitpay.app" 

    print("🔌 Conectando ao banco de dados...")
    
    with rx.session() as session:
        # Verifica se já existe a configuração
        statement = select(GatewayConfig).where(GatewayConfig.name == "suitpay")
        gateway = session.exec(statement).first()

        creds_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "base_url": BASE_URL
        }

        config_data = {
            "webhook_url": "/api/payment/webhook/suitpay",
            "min_amount": 1.00
        }

        if gateway:
            print("🔄 Atualizando configuração da SuitPay...")
            gateway.credentials = creds_data
            gateway.config = config_data
            gateway.is_active = True
            gateway.is_sandbox = True
        else:
            print("✨ Criando nova configuração da SuitPay...")
            gateway = GatewayConfig(
                name="suitpay",
                is_active=True,
                is_sandbox=True,
                credentials=creds_data,
                config=config_data
            )
            session.add(gateway)
        
        session.commit()
        print("✅ Configuração SuitPay salva com sucesso!")

if __name__ == "__main__":
    init_suitpay_config()