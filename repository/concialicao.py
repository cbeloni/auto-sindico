from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.database import criar_engine
from repository.despesas import Despesa
from repository.caixa import Caixa

Base = declarative_base()

engine = criar_engine()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def concialiacao_ordenadas_por_id_desc():
    concialiacoes = session.query(Despesa, Caixa).join(Caixa, (Despesa.mes == Caixa.mes) & (Despesa.ano == Caixa.ano), isouter=True).order_by(Despesa.id.desc()).all()
    return [concialiacao.Despesa.to_dict() | (concialiacao.Caixa.to_dict() if concialiacao.Caixa else {}) for concialiacao in concialiacoes]