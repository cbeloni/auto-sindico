from datetime import datetime
from config.database import criar_conexao
from pydantic import BaseModel
from typing import Literal

class Extrato(BaseModel):
    banco: str
    data: str
    transacao: str
    tipo_transacao: str
    identificacao: str
    valor: float
    codigo_transacao: str

    def __init__(self, banco: str, data: str, transacao: str, tipo_transacao: str, identificacao: str, valor: float, codigo_transacao: str):
        super().__init__(banco=banco, data=data, transacao=transacao, tipo_transacao=tipo_transacao, identificacao=identificacao, valor=valor, codigo_transacao=codigo_transacao)


class ExtratoRepository:
    def __init__(self):
        self.db = criar_conexao()
    
    def salvar(self, registro: Extrato):
        cursor = self.db.cursor()
        query = """
        INSERT INTO extrato (banco, data, transacao, tipo_transacao, identificacao, valor, codigo_transacao) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        from datetime import datetime
        date_formatted = datetime.strptime(registro.data, "%d/%m/%Y").strftime("%Y-%m-%d")
        values = (registro.banco, date_formatted, registro.transacao, registro.tipo_transacao, registro.identificacao, registro.valor, registro.codigo_transacao)
        cursor.execute(query, values)
        self.db.commit()
        
    def consultar(self, data_inicio: str, data_fim: str) -> list[Extrato]:
        cursor = self.db.cursor()
        query = """
        SELECT banco, data, transacao, tipo_transacao, identificacao, valor, codigo_transacao
        FROM extrato 
        WHERE data BETWEEN %s AND %s
        """
        data_inicio_formatted = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_fim_formatted = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor.execute(query, (data_inicio_formatted, data_fim_formatted))
        resultados = cursor.fetchall()
        return [Extrato(banco=row[0], data=row[1].strftime("%d/%m/%Y"), transacao=row[2], tipo_transacao=row[3], identificacao=row[4], valor=row[5], codigo_transacao=row[6]) for row in resultados]
    
    def consultar_tipo_transacao(self, data_inicio: str, data_fim: str, tipo_transacao: str) -> list[Extrato]:
        cursor = self.db.cursor()
        query = """
        SELECT banco, data, transacao, tipo_transacao, identificacao, valor, codigo_transacao
        FROM extrato 
        WHERE data BETWEEN %s AND %s
        AND tipo_transacao = %s
        """
        data_inicio_formatted = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_fim_formatted = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor.execute(query, (data_inicio_formatted, data_fim_formatted, tipo_transacao))
        resultados = cursor.fetchall()
        return [Extrato(banco=row[0], data=row[1].strftime("%d/%m/%Y"), transacao=row[2], tipo_transacao=row[3], identificacao=row[4], valor=row[5], codigo_transacao=row[6]) for row in resultados]