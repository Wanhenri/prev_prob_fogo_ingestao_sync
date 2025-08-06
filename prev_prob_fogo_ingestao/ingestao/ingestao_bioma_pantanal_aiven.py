import os
from pathlib import Path

import geopandas as gpd
from dotenv import load_dotenv
from geoalchemy2 import Geometry
from sqlalchemy import create_engine

# Carrega variáveis do arquivo .env
load_dotenv()

# Lê a URL do banco de dados
engine_url = os.getenv('DB_URL')

# Caminho para o shapefile
# 1. Carregar o CSV
path = Path('/mnt/c/Users/WHS/Documents')

path_project = Path(f'{path}/prev_prob_fogo_ingestao')

base_path = Path(f'{path}/{path_project}/data/raw/Pantanal/')
shapefile_path = base_path / 'biome_border.shp'

# Conexão com o banco de dados
engine = create_engine(engine_url)


# Ler shapefile
gdf = gpd.read_file(shapefile_path)


# Confirmar e definir sistema de referência (CRS)
# Confirmar e definir sistema de referência (CRS)
CRS_var = 4674
if gdf.crs is None or gdf.crs.to_epsg() != CRS_var:
    gdf = gdf.to_crs(epsg=CRS_var)

# Renomear coluna de geometria e definir como ativa
gdf = gdf.rename(columns={'geometry': 'geom'})
gdf = gdf.set_geometry('geom')


# Escrever no banco de dados (PostGIS)
gdf.to_postgis(
    name='pantanal',
    con=engine,
    if_exists='replace',  # ou "append" se já existir
    index=False,
    dtype={'geom': Geometry(geometry_type='MULTIPOLYGON', srid=4674)},
)


print('✅ Dados dos biomas inseridos no PostGIS com sucesso.')
