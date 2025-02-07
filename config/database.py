from dotenv import load_dotenv, dotenv_values
import logging
import mysql.connector

load_dotenv()
_config = dotenv_values(".env")


# Função para criar a conexão com o banco de dados
def criar_conexao(config=None):
    global _config

    if not _config and not config:
        raise ValueError("É necessário fornecer um valor para o parâmetro 'config'")

    if not _config:
        _config = config

    connection = mysql.connector.connect(
        host=_config['host'],
        user=_config['user'],
        password=_config['password'],
        database=_config['database']
    )
    
    logging.info(f"conectado: {connection.is_connected()}")
    
    return connection