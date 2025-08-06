import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(
    dotenv_path='/mnt/c/Users/WHS/Documents/prev_prob_fogo_ingestao/prev_prob_fogo_ingestao/.env'
)


def db_engine():
    """Cria e retorna o engine de conexão para o banco de dados."""
    DB_URL = os.getenv('DB_URL')
    engine_url = DB_URL
    engine = create_engine(engine_url)
    return engine


with db_engine().connect() as conn:
    result = conn.execute(
        text(
            'SELECT * '
            'FROM biomas.previsao_2025 '
            'WHERE TRIM("SIGLA_UF") ILIKE :uf;'
        ),
        {'uf': 'ms'},
    )
    for row in result:
        print(row)
