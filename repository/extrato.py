from config.database import criar_conexao
from pydantic import BaseModel
from typing import Literal

class Extrato(BaseModel):
    data: str
    transacao: str
    tipo_transacao: str
    identificacao: str
    valor: float

    def __init__(self, data: str, transacao: str, tipo_transacao: str, identificacao: str, valor: float):
        super().__init__(data=data, transacao=transacao, tipo_transacao=tipo_transacao, identificacao=identificacao, valor=valor)


class ExtratoRepository:
    def __init__(self):
        self.db = criar_conexao()
    
    def salvar_registro(self, registro: Extrato):
        cursor = self.db.cursor()
        query = """
        INSERT INTO extrato (data, transacao, tipo_transacao, identificacao, valor) 
        VALUES (%s, %s, %s, %s, %s)
        """
        from datetime import datetime
        date_formatted = datetime.strptime(registro.data, "%d/%m/%Y").strftime("%Y-%m-%d")
        values = (date_formatted, registro.transacao, registro.tipo_transacao, registro.identificacao, registro.valor)
        cursor.execute(query, values)
        self.db.commit()