import logging
import os
from datetime import datetime
from typing import Optional

import requests
from dotenv import load_dotenv

from repository.extrato import Extrato, ExtratoRepository
from service.extrato.extrato_abstract import ExtratoAbstract

load_dotenv()

CLIENT_ID = os.getenv('PLUGGY_CLIENT_ID')
CLIENT_SECRET = os.getenv('PLUGGY_CLIENT_SECRET')
BASE_URL = os.getenv('PLUGGY_BASE_URL', 'https://api.pluggy.ai')
PAGE_SIZE = os.getenv('PLUGGY_PAGE_SIZE', 500)


class TokenPluggyService:

    def obter_token(self) -> Optional[str]:
        url = f"{BASE_URL}/auth"
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        data = {
            'clientId': CLIENT_ID,
            'clientSecret': CLIENT_SECRET
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('apiKey')

class ExtratoPluggyService(ExtratoAbstract):
    def obter_extrato(self, data_inicial: str, data_final: str) -> list[dict]:
        token_service = TokenPluggyService()
        api_key = token_service.obter_token()
        if not api_key:
            raise Exception("Failed to obtain API key from Pluggy.")

        url = f"{BASE_URL}/transactions"
        headers = {
            'accept': 'application/json',
            'x-api-key': api_key
        }
        params = {
            'accountId': '99f7d3e6-df44-48dd-bb6a-bc012224707f',
            'pageSize': PAGE_SIZE,
            'from': data_inicial,
            'to': data_final,
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def gravar_extrato(self, extrato: list[dict]) -> None:
        extrato_repository = ExtratoRepository()
        for item in extrato["results"]:
            date_str = item.get('date')
            formatted_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%d/%m/%Y') if date_str else ''

            extrato_item = Extrato(
                banco="pluggy",
                data=formatted_date,
                transacao=item.get('operationType', ''),
                tipo_transacao=item.get('type', ''),
                identificacao=item.get('description', ''),
                valor=float(item.get('amount', 0.0)),
                codigo_transacao=item.get('id', '')
            )
            try:
                extrato_repository.salvar(extrato_item)
            except Exception as e:
                logging.error(f"Erro ao salvar extrato: {e}")
