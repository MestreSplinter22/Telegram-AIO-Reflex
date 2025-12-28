from dashboard.backend.models.models import GatewayConfig
from dashboard.backend.gateways.efi_service import EfiPixService
import requests

# Simula sua config (Preencha com os dados reais se não quiser ler do DB)
config_mock = GatewayConfig()
config_mock.is_sandbox = False # PRODUÇÃO
config_mock.credentials = {
    "client_id": "Client_Id_2d0a029fbb64d23dcd8fc0af4046f26e4e603046",
    "client_secret": "Client_Secret_c36a41b56fa508b9b2400346b30a9bf7fb03881e",
    "certificate_path": "dashboard/backend/api/gateways/efi/credencial/producao.p12",
    "certificate_password": "", # Se tiver senha
    "pix_key": "5726ec81-0287-4657-b68d-90f6d9629b2e" # Sua chave atual
}

service = EfiPixService(config_mock)

try:
    print("1. Tentando Autenticar...")
    token = service.authenticate()
    print(f"✅ Autenticado! Token: {token[:10]}...")

    print("\n2. Listando Chaves da Conta...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    with service._get_cert_context() as cert:
        response = requests.get(f"{service.env_url}/v2/gn/evp", headers=headers, cert=cert)
        print(f"Status Chaves: {response.status_code}")
        print(f"Resposta Chaves: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")