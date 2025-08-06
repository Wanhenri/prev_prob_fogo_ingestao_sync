from sqlalchemy import create_engine, text


def db_engine():
    """Cria e retorna o engine de conexão para o banco de dados."""
    DB_URL = 'postgresql://neondb_owner:*******@ep-calm-sun-acqqs9yf-pooler.sa-east-1.aws.neon.tech/******?sslmode=require&channel_binding=require'
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
