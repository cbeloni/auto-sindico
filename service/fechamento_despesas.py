from datetime import datetime
from dto.fechamento_requests import get_transacao_debito
from repository.despesas import Despesa
from repository.extrato import ExtratoRepository
from util.datas_uteis import meses_portugues

identificacao_sabesp = ['sabesp','cia de saneamento basico',]
identificacao_enel = ['enel',]
identificacao_outros = ['ecoville',]

def fechar_despesas(data_inicial, data_final):
    extrato_repository = ExtratoRepository()

    resultados = extrato_repository.consultar(data_inicial, data_final)

    despesas = {'faxina': 0, 'enel': 0, 'sabesp': 0, 'outros': 0}
    for resultado in resultados:
        if 'edileuza' in resultado.identificacao.lower() and resultado.tipo_transacao == get_transacao_debito(resultado.banco):
            despesas['faxina'] += resultado.valor
        elif any(item in resultado.identificacao.lower() for item in identificacao_enel) and resultado.tipo_transacao == get_transacao_debito(resultado.banco):
            despesas['enel'] += resultado.valor
        elif any(item in resultado.identificacao.lower() for item in identificacao_sabesp) and resultado.tipo_transacao == get_transacao_debito(resultado.banco):
            despesas['sabesp'] += resultado.valor
        elif any(item in resultado.identificacao.lower() for item in identificacao_outros) and resultado.tipo_transacao == get_transacao_debito(resultado.banco):
            despesas['outros'] += resultado.valor
    
    mes = meses_portugues[datetime.strptime(data_inicial, "%d/%m/%Y").strftime("%B")]
    ano = datetime.strptime(data_inicial, "%d/%m/%Y").year
    
    despesa = Despesa(
        mes=mes,
        ano=ano,
        enel=despesas['enel']*-1,
        sabesp=despesas['sabesp']*-1,
        faxina=despesas['faxina']*-1,
        outros=despesas['outros']*-1
    )
    despesa.save()
    return despesa.to_dict()