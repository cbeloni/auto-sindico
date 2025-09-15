
from pydantic import BaseModel

from util.datas_uteis import first_day_of_current_month, last_day_of_current_month, last_day_of_previous_month

class FechamentoRequest(BaseModel):
    data_inicial: str = last_day_of_previous_month()
    data_final: str = last_day_of_current_month()


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