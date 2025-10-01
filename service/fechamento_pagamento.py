from datetime import datetime
import logging
from dto.fechamento_requests import get_transacao_credito
from repository.caixa import Caixa
from repository.despesas import despesas_por_data
from repository.extrato import ExtratoRepository
from util.datas_uteis import meses_portugues
from util.identificadores import apartamento1, apartamento2, apartamento3, apartamento4
from decimal import Decimal

def fechar_pagamentos(data_inicial, data_final):
    logging.info(f"Fechando pagamentos de {data_inicial} até {data_final}")
    extrato_repository = ExtratoRepository()
    
    pagamentos = {'apartamento1': 0, 'apartamento2': 0, 'apartamento3': 0, 'apartamento4': 0}

    resultados = extrato_repository.consultar(data_inicial, data_final)
    for resultado in resultados:
        if any(ap1 in resultado.identificacao.lower() for ap1 in apartamento1) \
           and resultado.tipo_transacao == get_transacao_credito(resultado.banco):
            pagamentos['apartamento1'] += resultado.valor
        elif any(ap2 in resultado.identificacao.lower() for ap2 in apartamento2) \
           and resultado.tipo_transacao == get_transacao_credito(resultado.banco):
            pagamentos['apartamento2'] += resultado.valor
        elif any(ap3 in resultado.identificacao.lower() for ap3 in apartamento3) \
           and resultado.tipo_transacao == get_transacao_credito(resultado.banco):
            pagamentos['apartamento3'] += resultado.valor
        elif any(ap4 in resultado.identificacao.lower() for ap4 in apartamento4) \
           and resultado.tipo_transacao == get_transacao_credito(resultado.banco):
            pagamentos['apartamento4'] += resultado.valor
            
    mes = meses_portugues[datetime.strptime(data_inicial, "%d/%m/%Y").strftime("%B")]
    ano = datetime.strptime(data_inicial, "%d/%m/%Y").year
    
    caixa = Caixa(
        mes=mes,
        ano=ano,
        pagamentos_ap1=pagamentos['apartamento1'],
        pagamentos_ap2=pagamentos['apartamento2'],
        pagamentos_ap3=pagamentos['apartamento3'],
        pagamentos_ap4=pagamentos['apartamento4']
    )        
    
    despesas = despesas_por_data(mes, ano)    

    caixa.caixa_ap1 = max(round(Decimal(caixa.pagamentos_ap1) - despesas['valor_mensal_ap1'], 2), 0)
    caixa.caixa_ap2 = max(round(Decimal(caixa.pagamentos_ap2) - despesas['valor_mensal_ap2'], 2), 0)
    caixa.caixa_ap3 = max(round(Decimal(caixa.pagamentos_ap3) - despesas['valor_mensal_ap3'], 2), 0)
    caixa.caixa_ap4 = max(round(Decimal(caixa.pagamentos_ap4) - despesas['valor_mensal_ap4'], 2), 0)
    
    caixa_atualizado = caixa.save()
    return caixa_atualizado