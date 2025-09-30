from typing import Dict
from service.extrato.extrato_abstract import ExtratoAbstract
from service.extrato.mercadopago import ExtratoMercadoPagoService
from service.extrato.pluggy import ExtratoPluggyService


def factory_extrato_service(service_name: str) -> ExtratoAbstract:
    services: Dict[str, ExtratoAbstract] = {
        'pluggy': ExtratoPluggyService(),
        'mercadopago': ExtratoMercadoPagoService(),
    }
    return services.get(service_name)