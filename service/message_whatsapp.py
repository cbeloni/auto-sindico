def montar_messagem_whatsapp(transacoes: list[dict]) -> str:
    mensagens = []
    for i, mes_dados in enumerate(transacoes[:2]):
        mensagem = ""

        # Adiciona o cabeçalho do mês e despesas
        mensagem += f"*Referente a {mes_dados['mes']}/{mes_dados['ano']}*\n"
        mensagem += f"*Despesas:* R$ {mes_dados['total']}\n"
        mensagem += f"- *Enel:* R$ {mes_dados['enel']}\n"
        mensagem += f"- *Sabesp:* R$ {mes_dados['sabesp']}\n"
        mensagem += f"- *Faxina:* R$ {mes_dados['faxina']}\n"
        mensagem += f"- *Outros:* R$ {mes_dados['outros']}\n"
        # Verifica se existem chaves de pagamento no dicionário do mês
        if 'pagamentos_ap1' in mes_dados:
            mensagem += "*Pagamentos realizados:*\n"
            # Itera de 1 a 4 para montar a lista de pagamentos dos apartamentos
            for ap_num in range(1, 5):
                chave_pagamento = f"pagamentos_ap{ap_num}"
                valor_pago = mes_dados.get(chave_pagamento, '0.00') # Usa .get para segurança
                mensagem += f"- *Ap {ap_num}:* R$ {valor_pago}\n"
        else:
            # Adiciona a mensagem de que não há pagamentos registrados
            mensagem += "_(Nenhum pagamento registrado para este mês)_\n"
        mensagens.append(mensagem.strip())

    return mensagens