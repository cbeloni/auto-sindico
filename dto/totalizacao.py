from decimal import Decimal

apartamentos = ["pagamentos_ap1", "pagamentos_ap2", "pagamentos_ap3", "pagamentos_ap4"]

def calcular_totais(despesas):
    total_caixa = sum(despesa.get("caixa_total", 0) for despesa in despesas)
    total_pagamentos = 0
    for apartamento in apartamentos:
        total_pagamentos += sum(despesa.get(apartamento, 0) for despesa in despesas)
    total_despesas = sum(despesa.get("total", 0) for despesa in despesas)
    pendete_pagamento = Decimal(total_despesas) - (Decimal(total_pagamentos) - Decimal(total_caixa))
    saldo = total_caixa - pendete_pagamento
    totais = {
        "total_caixa": total_caixa,
        "total_pagamentos": total_pagamentos,
        "total_despesas": total_despesas,
        "pendente_pagamento": pendete_pagamento,
        "saldo": saldo,
    }
    return totais