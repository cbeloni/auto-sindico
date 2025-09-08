def montar_messagem_whatsapp(transacoes: list[dict]) -> str:
    mensagem = ""
    
    for i, mes_dados in enumerate(transacoes[:2]):
        # Adiciona um separador antes do segundo item
        if i > 0:
            mensagem += "\n---\n\n"

        # Adiciona o cabeçalho do mês e o total de despesas
        mensagem += f"*Referente a {mes_dados['mes']}/{mes_dados['ano']}*\n"
        mensagem += f"*Total de despesas:* R$ {mes_dados['total']}\n"

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

    # Imprime a mensagem final, removendo espaços extras no final
    print(mensagem.strip())
    return mensagem.strip()