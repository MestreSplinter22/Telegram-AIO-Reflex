# init_gateway.py
import reflex as rx
from sqlmodel import select
from dashboard.backend.models.models import GatewayConfig

def init_efi_config():
    # Dados fornecidos
    CLIENT_ID = "Client_Id_608af48df53f60cbf3334bcdbfcae7e55e500dfb"
    CLIENT_SECRET = "Client_Secret_3dd34db98922459e02291fcd96777cf530c4316a"
    CERT_PATH = "dashboard/backend/api/gateways/efi/credencial/producao.p12"
    
    # --- IMPORTANTE: COLOQUE SUA CHAVE PIX ABAIXO ---
    PIX_KEY = "5726ec81-0287-4657-b68d-90f6d9629b2e" 
    # ------------------------------------------------

    print("🔌 Conectando ao banco de dados...")
    
    with rx.session() as session:
        # Verifica se já existe a configuração
        statement = select(GatewayConfig).where(GatewayConfig.name == "efi_bank")
        gateway = session.exec(statement).first()

        # Estrutura das credenciais (JSON)
        creds_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "certificate_path": CERT_PATH,
            "certificate_password": "", # Senha vazia conforme padrão Efí
            "pix_key": PIX_KEY
        }

        # Configurações extras (URLs, limites, etc)
        config_data = {
            "webhook_url": "/api/payment/webhook/efi",
            "min_amount": 1.00
        }

        if gateway:
            print("🔄 Atualizando configuração existente da Efí Bank...")
            gateway.credentials = creds_data
            gateway.config = config_data
            gateway.is_active = True
            gateway.is_sandbox = True # True = Homologação
        else:
            print("✨ Criando nova configuração da Efí Bank...")
            gateway = GatewayConfig(
                name="efi_bank",
                is_active=True,
                is_sandbox=True, # True = Homologação
                credentials=creds_data,
                config=config_data
            )
            session.add(gateway)
        
        session.commit()
        session.refresh(gateway)
        print(f"✅ Configuração salva com sucesso! ID: {gateway.id}")
        print(f"📂 Certificado configurado em: {gateway.credentials['certificate_path']}")

if __name__ == "__main__":
    init_efi_config()