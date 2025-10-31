from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from config.database import get_session

Base = declarative_base()

class FechamentoDespesas(Base):
    __tablename__ = 'fechamento_despesas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mes = Column(String(255), nullable=False)
    ano = Column(Integer, nullable=False)
    apartamento = Column(String)
    valor = Column(DECIMAL)
    qrcode = Column(String)
    brcode = Column(String)
    url_qrcode = Column(String)
    status = Column(String)
    data_atual = Column(String, nullable=True)

    def save(self):
        session = get_session()
        existing_record = session.query(FechamentoDespesas).filter_by(mes=self.mes, ano=self.ano, apartamento=self.apartamento).first()
        if existing_record:
            session.delete(existing_record)
            session.commit()
        session.add(self)
        session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'mes': self.mes,
            'ano': self.ano,
            'apartamento': self.apartamento,
            "valor": self.valor,
            'qrcode': self.qrcode,
            'brcode': self.brcode,
            'url_qrcode': self.url_qrcode,
            'status': self.status
        }
        
def fechamento_despesas_pendentes(mes, ano):
    session = get_session()
    return session.query(FechamentoDespesas).filter_by(mes=mes, ano=ano).filter(FechamentoDespesas.status == None).all()

def fechamento_despesas_status(mes, ano, status, apartamento):
    session = get_session()
    return session.query(FechamentoDespesas).filter_by(mes=mes, ano=ano, status=status, apartamento=apartamento).all()

def get_last_fechamento_despesas() -> FechamentoDespesas:
    session = get_session()
    return session.query(FechamentoDespesas).order_by(FechamentoDespesas.id.desc()).first()

def marcar_status(mes, ano, apartamento, status):
    session = get_session()
    record = session.query(FechamentoDespesas).filter_by(mes=mes, ano=ano, apartamento=apartamento).first()
    if record:
        record.status = status
        session.commit()