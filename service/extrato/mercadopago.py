from datetime import datetime
import logging
import os
from repository.extrato import Extrato
from service.extrato.extrato_abstract import ExtratoAbstract
import requests


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
MERCADOPAGO_COOKIE = os.getenv('MERCADOPAGO_COOKIE')

class ExtratoMercadoPagoService(ExtratoAbstract):

    def obter_extrato(self) -> list[dict]:
        headers = {
            'User-Agent': USER_AGENT,
            'Cookie': MERCADOPAGO_COOKIE
        }

        response = requests.get(
            'https://www.mercadopago.com.br/banking/balance/movements/api/list',
            params={
                'client_id': 'open-finance',
                'period': 'last_month',
                'currency_id': 'BRL',
                'bank_id': '3655a3e2-a1b8-4e80-8d3f-e9344ae92ac8',
                'account_id': '4d2ce011-b749-5ab2-8fa2-f7ba5d55f585'
            },
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    
    def gravar_extrato(self, extrato: list[dict]) -> None:
        from repository.extrato import ExtratoRepository
        extrato_repository = ExtratoRepository()
        all_movements = [movement for b in extrato["binnacles"] for movement in b["movements"]]

        for item in all_movements:
            date_str = item.get('ledger_datetime')
            formatted_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%d/%m/%Y') if date_str else ''
            amount_data = item.get('amount', {})
            fraction = float(amount_data.get('fraction', '0'))
            cents = float(amount_data.get('cents', '0')) / 100
            amount = fraction + cents
            tipo_transacao = item.get('metadata', {}).get('type', '')

            extrato_item = Extrato(
                banco="mercadopago",
                data=formatted_date,
                transacao=item.get('title', ''),
                tipo_transacao=tipo_transacao,
                identificacao=item.get('description', ''),
                valor=amount,
                codigo_transacao=item.get('id', '')
            )
            try:
                extrato_repository.salvar(extrato_item)
            except Exception as e:
                logging.error(f"Erro ao salvar extrato: {e}")