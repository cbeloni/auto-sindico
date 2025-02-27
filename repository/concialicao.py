from config.database import criar_sessao
from config.database_async import Database
from repository.despesas import Despesa
from repository.caixa import Caixa

database = Database()

def concialiacao_ordenadas_por_id_desc():
    session = database.get_session()
    concialiacoes = session.query(Despesa, Caixa).join(Caixa, (Despesa.mes == Caixa.mes) & (Despesa.ano == Caixa.ano), isouter=True).order_by(Despesa.id.desc()).all()
    return [concialiacao.Despesa.to_dict() | (concialiacao.Caixa.to_dict() if concialiacao.Caixa else {}) for concialiacao in concialiacoes]