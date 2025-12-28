import os
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives import serialization

# --- CONFIGURAÇÃO ---
# Coloque o nome exato do arquivo que você baixou da Efí
ARQUIVO_ENTRADA_P12 = "dashboard/backend/api/gateways/efi/credencial/producao.p12"  
ARQUIVO_SAIDA_PEM = "certificado.pem"
# Normalmente a Efí gera o p12 sem senha, mas se tiver, coloque b"suasenha"
SENHA_P12 = None   

def converter():
    if not os.path.exists(ARQUIVO_ENTRADA_P12):
        print(f"❌ Erro: O arquivo '{ARQUIVO_ENTRADA_P12}' não foi encontrado na pasta.")
        return

    print(f"🔓 Abrindo o arquivo {ARQUIVO_ENTRADA_P12}...")

    try:
        with open(ARQUIVO_ENTRADA_P12, "rb") as f:
            p12_data = f.read()

        # Extrai a chave e o certificado do arquivo P12
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
            p12_data,
            password=SENHA_P12
        )

        print(f"⚙️  Convertendo para formato PEM...")

        with open(ARQUIVO_SAIDA_PEM, "wb") as f:
            # 1. Escreve a Chave Privada (descriptografada)
            if private_key:
                f.write(private_key.private_bytes(
                    encoding=Encoding.PEM,
                    format=PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=NoEncryption()
                ))
            
            # 2. Escreve o Certificado Público
            if certificate:
                f.write(certificate.public_bytes(Encoding.PEM))
            
            # 3. Escreve certificados extras (Cadeia de certificação), se houver
            if additional_certificates:
                for cert in additional_certificates:
                    f.write(cert.public_bytes(Encoding.PEM))

        print(f"✅ Sucesso! Arquivo '{ARQUIVO_SAIDA_PEM}' criado.")
        print("👉 Agora você pode usar este arquivo no SDK da Efí.")

    except Exception as e:
        print(f"❌ Erro ao converter: {e}")

if __name__ == "__main__":
    converter()