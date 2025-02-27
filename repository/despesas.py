from sqlalchemy import  Column, Integer, String, DECIMAL, Computed
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.database import criar_sessao
from config.database_async import Database

Base = declarative_base()
database = Database()
class Despesa(Base):
    __tablename__ = 'despesas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mes = Column(String(255), nullable=False)
    ano = Column(Integer, nullable=False)
    enel = Column(DECIMAL(10, 2), nullable=False)
    sabesp = Column(DECIMAL(10, 2), nullable=False)
    faxina = Column(DECIMAL(10, 2), nullable=False)
    outros = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), Computed('enel + sabesp + faxina + outros'), nullable=False)
    valor_mensal_ap1 = Column(DECIMAL(10, 2), Computed('total / 4'), nullable=False)
    valor_mensal_ap2 = Column(DECIMAL(10, 2), Computed('total / 4'), nullable=False)
    valor_mensal_ap3 = Column(DECIMAL(10, 2), Computed('total / 4'), nullable=False)
    valor_mensal_ap4 = Column(DECIMAL(10, 2), Computed('total / 4'), nullable=False)

    def save(self):
        session = database.get_session()
        existing_record = session.query(Despesa).filter_by(mes=self.mes, ano=self.ano).first()
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
            'enel': self.enel,
            'sabesp': self.sabesp,
            'faxina': self.faxina,
            'outros': self.outros,
            'total': self.total,
            'valor_mensal_ap1': self.valor_mensal_ap1,
            'valor_mensal_ap2': self.valor_mensal_ap2,
            'valor_mensal_ap3': self.valor_mensal_ap3,
            'valor_mensal_ap4': self.valor_mensal_ap4,
        }
        
def despesas_por_data(mes, ano):
    session = database.get_session()
    existing_record = session.query(Despesa).filter_by(mes=mes, ano=ano).first()
    return existing_record.to_dict()

def despesas_ordenadas_por_id_desc():
    session = database.get_session()
    despesas = session.query(Despesa).order_by(Despesa.id.desc()).all()
    return [despesa.to_dict() for despesa in despesas]
    
if __name__ == '__main__':
    # Database connection
    engine = criar_sessao()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    despesas_dict = {'faxina': 0, 'enel': 0, 'sabesp': 0, 'outros': 0}

    despesa_exemplo = Despesa(
        mes='Janeiro',
        ano=2023,
        enel=despesas_dict['enel'],
        sabesp=despesas_dict['sabesp'],
        faxina=despesas_dict['faxina'],
        outros=despesas_dict['outros']
    )

    # Add the object to the session and commit to save it in the database
    session.add(despesa_exemplo)
    session.commit()
    
    