import os
from pathlib import Path

import geopandas as gpd
from dotenv import load_dotenv


def carregar_e_processar_dados(ano: int, trimestre: str) -> gpd.GeoDataFrame:
    """
    Carrega o shapefile, confirma o CRS, e adiciona colunas de ano e trimestre.
    """
    path = Path('/mnt/c/Users/WHS/Documents')

    path_project = Path(f'{path}/prev_prob_fogo_ingestao')

    # 1. Carregar o CSV
    base_path = Path(f'{path_project}/data/raw/previsao_{ano}/{trimestre}')

    file_trimestre = f'{trimestre}_Cptec_CD_MUN_tabela_completa.shp'

    shapefile_path = base_path / file_trimestre

    if not shapefile_path.exists():
        raise FileNotFoundError(f'Arquivo nao encontrado: {shapefile_path}')


def main():
    """
    Função principal que orquestra o fluxo de trabalho.
    """
    # Carrega variáveis do arquivo .env
    load_dotenv()

    # Lê a URL do banco de dados
    engine_url = os.getenv('DB_URL')

    if not engine_url:
        raise ValueError("Variável de ambiente 'DB_URL' não definida ")

    ano = 2025
    trimestre = 'JAS'

    try:
        gdf = carregar_e_processar_dados(ano, trimestre)
        print(gdf)
    except Exception as e:
        print(f'Ocorreu um erro: {e}')


if __name__ == '__main__':
    main()
