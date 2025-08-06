import pandas as pd
from sqlalchemy import create_engine

# 1. Carregar o CSV
df = pd.read_csv('ASO_Cptec_CD_MUN_Centro-Oeste.csv')

# 2. Padronizar colunas (evita erros de escrita)
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# 3. Conectar ao banco PostgreSQL
# Substitua com seus dados: usuário, senha, host, porta e banco
engine = create_engine(
    'postgresql://neondb_owner:******@ep-calm-sun-acqqs9yf-pooler.sa-east-1.aws.neon.tech/******?sslmode=require&channel_binding=require'
)

# 4. Inserir os dados
df.to_sql('clima_municipal', con=engine, if_exists='append', index=False)

print('Ingestão concluída com sucesso.')
