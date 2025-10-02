
import logging
from pydantic import BaseModel

from repository.fechamento_despesas import get_last_fechamento_despesas
from util.datas_uteis import first_day_of_current_month, format_date_to_ddmmyyyy, last_day_of_current_month, last_day_of_previous_month

class FechamentoRequest(BaseModel):
    data_inicial: str = last_day_of_previous_month()
    data_final: str = last_day_of_current_month()

class FechamentoPagamentosDate():
    data_atual: str = get_last_fechamento_despesas().data_atual
    logging.info(f"Data atual do último fechamento de despesas: {data_atual}")
    data_inicial: str = format_date_to_ddmmyyyy(data_atual)
    logging.info(f"Data inicial do fechamento de pagamentos: {data_inicial}")
    data_final: str = last_day_of_current_month()
    logging.info(f"Data final do fechamento de pagamentos: {data_final}")


class FechamentoDespesasRequest(BaseModel):
    data_inicial: str = first_day_of_current_month()
    data_final: str = last_day_of_current_month()
    

def get_transacao_debito(banco: str) -> dict:
    transacao_map = {
        'cora': 'DÉBITO',
        'bb': 'Saída',
        'pagbank': 'Saída',
        "pluggy": 'DEBIT',
    }
    return transacao_map.get(banco, 'DÉBITO')


def get_transacao_credito(banco: str) -> dict:
    transacao_map = {
        'cora': 'CRÉDITO',
        'bb': 'Entrada',
        'pagbank': 'Entrada',
        "pluggy": 'CREDIT'
    }
    return transacao_map.get(banco, 'CRÉDITO')