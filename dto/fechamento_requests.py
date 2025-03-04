from pydantic import BaseModel
from datetime import datetime, timedelta


def first_day_of_current_month():
    today = datetime.today()
    return today.replace(day=1).strftime('%d/%m/%Y')

def last_day_of_previous_month():
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_previous_month.strftime('%d/%m/%Y')

def last_day_of_current_month():
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4) 
    return (next_month - timedelta(days=next_month.day)).strftime('%d/%m/%Y')

class FechamentoRequest(BaseModel):
    data_inicial: str = last_day_of_previous_month()
    data_final: str = last_day_of_current_month()
    

def get_transacao_debito(banco: str) -> dict:
    transacao_map = {
        'cora': 'DÉBITO',
        'bb': 'Saída'
    }
    return transacao_map.get(banco, 'DÉBITO')


def get_transacao_credito(banco: str) -> dict:
    transacao_map = {
        'cora': 'CRÉDITO',
        'bb': 'Entrada'
    }
    return transacao_map.get(banco, 'CRÉDITO')