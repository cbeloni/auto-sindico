from dto.fechamento_requests import first_day_of_current_month, last_day_of_current_month
from dto.resumo_requests import ResumoRequest
from repository.extrato import Extrato, ExtratoRepository


def consultar_tipo_transacao(request: ResumoRequest = None) -> list[Extrato]:
    extratoRepository = ExtratoRepository()
    extrato: list[Extrato] = extratoRepository.consultar_tipo_transacao(data_inicio=request.data_inicial, 
                                                                        data_fim=request.data_final, 
                                                                        tipo_transacao='avulso')
    return extrato