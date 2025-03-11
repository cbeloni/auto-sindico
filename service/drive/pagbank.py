import logging
from googleapiclient.http import MediaIoBaseDownload
import io
import csv

from repository.extrato import Extrato

def gravar_extrato_pagbank(service, file_id, extrato_repository):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    fh.seek(0)
    decoded_fh = io.StringIO(fh.read().decode("latin-1"))
    dict_reader = csv.DictReader(decoded_fh, delimiter=';')
    lista_extrato = []
    for row in dict_reader:
        valor = float(row['VALOR'].replace('.', '').replace(',', '.'))
        tipo_transacao = 'Saída' if valor < 0 else 'Entrada'
        extrato = Extrato('pagbank', row['DATA'], row['TIPO'], tipo_transacao, row['DESCRICAO'], valor, row['CODIGO DA TRANSACAO'])
        lista_extrato.append(extrato)

    for linha in lista_extrato:
        try:
            extrato_repository.salvar(linha)
        except Exception as e:
            logging.info(f"Error ao salvar extrato: {e}")
    return lista_extrato