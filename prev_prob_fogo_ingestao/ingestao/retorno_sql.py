import geopandas as gpd
from sqlalchemy import create_engine

# URL do banco de dados (ajuste se necessário)
db_url = 'postgresql://neondb_owner:******@ep-calm-sun-acqqs9yf-pooler.sa-east-1.aws.neon.tech/******?sslmode=require&channel_binding=require'

# Criação do engine
engine = create_engine(db_url)

# SQL para buscar todos os dados da UF 'MS'
sql = """
    SELECT *
    FROM biomas.clima_municipal
    WHERE "SIGLA_UF" = 'MS';
"""

gdf = gpd.read_postgis(sql, con=engine, geom_col='geometry')

# Mostrar as 5 primeiras linhas
print(gdf.head())
