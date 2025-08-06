import os
from pathlib import Path

import geopandas as gpd
from dotenv import load_dotenv
from geoalchemy2 import Geometry
from sqlalchemy import create_engine

ano = 2025
trimestre = 'JAS'

# Carrega variáveis do arquivo .env
load_dotenv()

# Lê a URL do banco de dados
engine_url = os.getenv('DB_URL')

# 1. Carregar o CSV
path = Path('/mnt/c/Users/WHS/Documents')

path_project = Path(f'{path}/prev_prob_fogo_ingestao')

# 1. Carregar o CSV
base_path = Path(f'{path_project}/data/raw/previsao_{ano}/{trimestre}')
"""
# base_path = Path(f"/mnt/c/Users/WHS/
# Documents/prev_prob_fogo_ingestao/
# prev_prob_fogo_ingestao/data/raw/
# previsao_{ano}/{trimestre}")

"""

shapefile_path = base_path / f'{trimestre}_Cptec_CD_MUN_tabela_completa.shp'

# Ler shapefile
gdf = gpd.read_file(shapefile_path)

# Confirmar e definir sistema de referência (CRS)
CRS_var = 4674
if gdf.crs is None or gdf.crs.to_epsg() != CRS_var:
    gdf = gdf.to_crs(epsg=CRS_var)


# ✅ Adiciona colunas ano e trimestre
gdf['ano'] = ano
gdf['trimestre'] = trimestre


# 3. Conectar ao banco PostgreSQL
# Substitua com seus dados: usuário, senha, host, porta e banco
engine = create_engine(engine_url)


gdf.to_postgis(
    name='previsao_2025',
    con=engine,
    schema='biomas',
    if_exists='replace',  # ou "append" se já existir
    index=False,
    dtype={'geom': Geometry(geometry_type='MULTIPOLYGON', srid=4674)},
)
