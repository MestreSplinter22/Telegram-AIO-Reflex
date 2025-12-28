# fix_efi_key.py
import reflex as rx
import requests
import json
from dashboard.backend.models.models import GatewayConfig
from dashboard.backend.gateways.efi_service import EfiPixService

def fix_key():
    print("🔧 Iniciando correção da Chave PIX de Homologação...")
    
    with rx.session() as session:
        # 1. Buscar a configuração atual
        gateway = session.query(GatewayConfig).filter(
            GatewayConfig.name == "efi_bank"
        ).first()
        
        if not gateway:
            print("❌ Erro: Nenhuma configuração encontrada no banco. Rode o init_gateway.py primeiro.")
            return

        print("🔑 Credenciais encontradas. Autenticando...")
        
        # 2. Instanciar o serviço para usar a autenticação que já criamos
        try:
            efi = EfiPixService(gateway)
            token = efi.authenticate()
            print("✅ Autenticação OK!")
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            print("Verifique se o Client_Id e Client_Secret estão corretos no init_gateway.py")
            return

        # 3. Criar uma Chave Aleatória (EVP) no Sandbox
        # Endpoint: POST /v2/gn/evp
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Usamos o contexto do certificado do serviço
        with efi._get_cert_context() as cert:
            response = requests.post(
                f"{efi.env_url}/v2/gn/evp",
                headers=headers,
                cert=cert,
                json={} # Payload vazio para gerar nova chave
            )
            
        if response.status_code == 201:
            data = response.json()
            new_key = data["chave"]
            print(f"🎉 Nova Chave de Testes Gerada: {new_key}")
            
            # 4. Salvar no Banco
            # Precisamos copiar o dict, modificar e salvar de volta para o SQLAlchemy detectar a mudança no JSON
            new_creds = gateway.credentials.copy()
            new_creds["pix_key"] = new_key
            
            gateway.credentials = new_creds
            session.add(gateway)
            session.commit()
            print("✅ Banco de dados atualizado com a nova chave!")
            print("🚀 Tente gerar o PIX no bot novamente.")
            
        else:
            print(f"❌ Erro ao criar chave: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fix_key()