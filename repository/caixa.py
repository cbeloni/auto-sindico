from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from config.database import get_session
from sqlalchemy.orm import column_property

Base = declarative_base()

class Caixa(Base):
    __tablename__ = 'caixa'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mes = Column(String(255), nullable=False)
    ano = Column(Integer, nullable=False)
    pagamentos_ap1 = Column(DECIMAL(10, 2), nullable=False)
    pagamentos_ap2 = Column(DECIMAL(10, 2), nullable=False)
    pagamentos_ap3 = Column(DECIMAL(10, 2), nullable=False)
    pagamentos_ap4 = Column(DECIMAL(10, 2), nullable=False)
    caixa_ap1 = Column(DECIMAL(10, 2), nullable=False)
    caixa_ap2 = Column(DECIMAL(10, 2), nullable=False)
    caixa_ap3 = Column(DECIMAL(10, 2), nullable=False)
    caixa_ap4 = Column(DECIMAL(10, 2), nullable=False)
    total = column_property(caixa_ap1 + caixa_ap2 + caixa_ap3 + caixa_ap4)

    def save(self):
        session = get_session()
        existing_record = session.query(Caixa).filter_by(mes=self.mes, ano=self.ano).first()
        if existing_record:
            session.delete(existing_record)
            session.commit()        
        session.add(self)
        session.commit()
        return self.to_dict()
        
    def to_dict(self):
        return {
            'mes': self.mes,
            'ano': self.ano,
            'pagamentos_ap1': self.pagamentos_ap1,
            'pagamentos_ap2': self.pagamentos_ap2,
            'pagamentos_ap3': self.pagamentos_ap3,
            'pagamentos_ap4': self.pagamentos_ap4,
            'caixa_ap1': self.caixa_ap1,
            'caixa_ap2': self.caixa_ap2,
            'caixa_ap3': self.caixa_ap3,
            'caixa_ap4': self.caixa_ap4,
            'caixa_total': self.total,
        }
        
def caixa_ordenado_por_id_desc():
    session = get_session()
    caixas = session.query(Caixa).order_by(Caixa.id.desc()).all()
    return [caixa.to_dict() for caixa in caixas]