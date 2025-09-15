from typing import Type, Optional
from typing import Type, Optional
from typing import Dict, Type, Optional
import os
import requests
from dotenv import load_dotenv

from repository.extrato import Extrato, ExtratoRepository

load_dotenv()

CLIENT_ID = os.getenv('PLUGGY_CLIENT_ID')
CLIENT_SECRET = os.getenv('PLUGGY_CLIENT_SECRET')
BASE_URL = os.getenv('PLUGGY_BASE_URL', 'https://api.pluggy.ai')
PAGE_SIZE = os.getenv('PLUGGY_PAGE_SIZE', 500)

def factory_extrato_service(service_name: str) -> Optional[Type]:
    services: Dict[str, Type] = {
        'pluggy': ExtratoPluggyService,
    }
    return services.get(service_name)()


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

class ExtratoPluggyService:
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
            'accountId': 'c9cab9a5-b910-4176-b79e-f7691c527603',
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
            extrato_item = Extrato(
                banco="pluggy",
                data=item.get('date'),
                transacao=item.get('operationType', ''),
                tipo_transacao=item.get('type', ''),
                identificacao=item.get('iddescription', ''),
                valor=float(item.get('amount', 0.0)),
                codigo_transacao=item.get('id', '')
            )
            extrato_repository.salvar(extrato_item)
