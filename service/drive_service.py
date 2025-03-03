from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import csv

from repository.extrato import Extrato
from repository.extrato import ExtratoRepository

import logging
import os 
from dotenv import load_dotenv

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
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        fh.seek(0)
        decoded_fh = io.StringIO(fh.read().decode("latin-1"))
        dict_reader = csv.DictReader(decoded_fh)
        lista_extrato = []
        for row in dict_reader:
            valor = float(row['Valor'].replace('.', '').replace(',', '.'))
            extrato = Extrato('bb', row['Data'], row['Lançamento'], row['Tipo Lançamento'] or 'informativo', row['Detalhes'] or 'informação de saldo', valor)
            lista_extrato.append(extrato)

        for linha in lista_extrato:
            try:
                extrato_repository.salvar(linha)
            except Exception as e:
                logging.info(f"Error ao salvar extrato: {e}")
        return lista_extrato

if __name__ == "__main__":
    get_last_file_from_drive()
