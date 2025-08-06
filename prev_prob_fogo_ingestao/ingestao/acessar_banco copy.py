from sqlalchemy import create_engine, text

DB_URL = 'postgresql+psycopg2://avnadmin:*****C@pg-1dce562c-wanhenri01-103a.d.aivencloud.com:12121/*****?sslmode=require'

engine_url = DB_URL
engine = create_engine(engine_url)

with engine.connect() as conn:
    result = conn.execute(
        text(
            'SELECT column_name '
            'FROM information_schema.columns '
            "WHERE table_schema = 'previsao' AND table_name = 'previsao_2025';"
        )
    )
    for row in result:
        print(row)
