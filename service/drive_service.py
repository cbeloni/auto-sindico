from googleapiclient.discovery import build
from repository.extrato import ExtratoRepository
import os 
from dotenv import load_dotenv

from service.drive.bb import gravar_extrato_bb
from datetime import datetime

from service.drive.pagbank import gravar_extrato_pagbank

load_dotenv()

API_KEY = os.environ.get('API_KEY')

# ID da pasta no Google Drive
FOLDER_ID = os.environ.get('FOLDER_ID')

def get_last_file_from_drive():
    extrato_repository = ExtratoRepository()
    service = build('drive', 'v3', developerKey=API_KEY)

    # Listar arquivos na pasta
    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents",
        orderBy='createdTime desc',
        pageSize=1,
        fields="files(id, name, createdTime)"
    ).execute()

    items = results.get('files', [])

    if not items:
        print('No files found.')
        return None

    # Pegar o último arquivo
    last_file = items[0]
    file_id = last_file['id']
    file_name = last_file['name']    
    if file_name.startswith("Extrato conta corrente"):
        lista_extrato = gravar_extrato_bb(service, file_id, extrato_repository)
        return lista_extrato
    
    current_year = datetime.now().year
    if file_name.startswith(str(current_year)) and file_name.endswith('.csv'):
        lista_extrato = gravar_extrato_pagbank(service, file_id, extrato_repository)
        return lista_extrato    
    
if __name__ == "__main__":
    get_last_file_from_drive()
