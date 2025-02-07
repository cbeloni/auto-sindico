from collections.abc import Generator
import csv
from repository.extrato import Extrato

def read_lines(file: Generator):
    # if part.get_content_maintype() == 'multipart':
    #     continue
    # if part.get('Content-Disposition') is None:
    #     continue

    # Verificar se o anexo é um arquivo CSV
    filename = file.get_filename()
    if filename and filename.endswith('.csv'):
        # Baixar o anexo
        file_data = file.get_payload(decode=True)
        csv_content = file_data.decode('utf-8')

        # Ler o conteúdo do CSV
        csv_reader = csv.reader(csv_content.splitlines())
        linhas = []

        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            data, transacao, tipo_transacao, identificacao, valor = row
            extrato = Extrato(data, transacao, tipo_transacao, identificacao, valor)
            linhas.append(extrato)
            
        return linhas