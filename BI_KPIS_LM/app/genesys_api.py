import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env automaticamente
load_dotenv()

# Lê as variáveis de ambiente
client_id = os.getenv("GENESYS_CLIENT_ID")
client_secret = os.getenv("GENESYS_CLIENT_SECRET")

# ATENÇÃO: Usando a região padrão (EUA) da Genesys Cloud
auth_url = "https://login.mypurecloud.com/oauth/token"
exports_url = "https://api.mypurecloud.com/api/v2/analytics/reporting/exports"
local_folder = "POWER_BI"  # Pasta onde estão os arquivos CSV locais

if not client_id or not client_secret:
    print("Erro: Defina as variáveis de ambiente GENESYS_CLIENT_ID e GENESYS_CLIENT_SECRET no arquivo .env.") 
    exit(1)

# 1. Autenticação OAuth2
data = {"grant_type": "client_credentials"}
response = requests.post(auth_url, data=data, auth=(client_id, client_secret))
access_token = response.json().get("access_token")
if not access_token:
    print("Erro ao autenticar:", response.text)
    exit(1)
headers = {"Authorization": f"Bearer {access_token}"}

# 2. Buscar exportações agendadas
response = requests.get(exports_url, headers=headers)
exports = response.json().get("entities", [])

# 3. Exibir todos os exports retornados para depuração
print("==== EXPORTS RETORNADOS PELA API ====")
for export in exports:
    print(export)
print("=====================================")

# 4. Filtrar exportações de dois dias atrás (D-2)
dois_dias_atras = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
arquivos_local = [
    "Base - Texto.csv",
    "Base - Voz.csv",
    "Base - Voz e Texto.csv",
    "Base - Gestão de entrega N1.csv", 
]

baixou_arquivo = False
for export in exports:
    export_date = export.get("dateCreated", "")[:10]
    export_name = export.get("name") + ".csv"
    if export_date == dois_dias_atras and export_name in arquivos_local:
        download_url = export.get("downloadUrl")
        if download_url:
            print(f"Baixando {export_name} de {dois_dias_atras}...")
            file_response = requests.get(download_url, headers=headers)
            if file_response.status_code == 200:
                local_path = os.path.join(local_folder, export_name)
                with open(local_path, "wb") as f:
                    f.write(file_response.content)
                print(f"{export_name} atualizado com sucesso!")
                baixou_arquivo = True
            else:
                print(f"Erro ao baixar {export_name}: {file_response.status_code}")

if not baixou_arquivo:
    print(f"Nenhum arquivo encontrado para a data {dois_dias_atras}.")

print("Processo finalizado.")