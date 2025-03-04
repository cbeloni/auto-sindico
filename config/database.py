from dotenv import load_dotenv, dotenv_values
import logging
from sqlalchemy import create_engine
import mysql.connector
from sqlalchemy.orm import sessionmaker

load_dotenv()
_config = dotenv_values(".env")


# Função para criar a conexão com o banco de dados
def criar_conexao(config=None):
    global _config

    if not _config and not config:
        raise ValueError("É necessário fornecer um valor para o parâmetro 'config'")

    if not _config:
        _config = config

    logging.info(f"config: {_config}")
    connection = mysql.connector.connect(
        host=_config['HOST'],
        user=_config['USER'],
        password=_config['PASSWORD'],
        database=_config['DATABASE']
    )
    
    logging.info(f"conectado: {connection.is_connected()}")
    
    return connection

def criar_engine(config=None):
    connection_url = f"mysql+mysqlconnector://{_config['USER']}:{_config['PASSWORD']}@{_config['HOST']}/{_config['DATABASE']}"
    engine = create_engine(connection_url, pool_pre_ping=True)
    
    logging.info("SQLAlchemy engine created with pool_pre_ping enabled")
    
    return engine

def get_session():
    engine = criar_engine()
    Session = sessionmaker(bind=engine)
    return Session()
