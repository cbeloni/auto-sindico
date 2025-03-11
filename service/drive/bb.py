import logging
from googleapiclient.http import MediaIoBaseDownload
import io
import csv

from repository.extrato import Extrato

def gravar_extrato_bb(service, file_id, extrato_repository):
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