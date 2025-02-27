from config.database import get_session
from repository.despesas import Despesa
from repository.caixa import Caixa


def concialiacao_ordenadas_por_id_desc():
    session = get_session()
    concialiacoes = session.query(Despesa, Caixa).join(Caixa, (Despesa.mes == Caixa.mes) & (Despesa.ano == Caixa.ano), isouter=True).order_by(Despesa.id.desc()).all()
    return [concialiacao.Despesa.to_dict() | (concialiacao.Caixa.to_dict() if concialiacao.Caixa else {}) for concialiacao in concialiacoes]