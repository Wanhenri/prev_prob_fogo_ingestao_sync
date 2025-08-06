from pathlib import Path

# from prev_prob_fogo_ingestao.ingestao import


def test_shapefile_path():
    """Fixture para simular o caminho de um arquivo."""

    ano = 2025
    trimestre = 'JAS'
    path = Path('/mnt/c/Users/WHS/Documents')
    name_shapefile = 'Cptec_CD_MUN_tabela_completa.shp'

    path_project = Path(f'{path}/prev_prob_fogo_ingestao')

    # 1. Carregar o CSV
    base_path = Path(f'{path_project}/data/raw/previsao_{ano}/{trimestre}')

    shapefile_path = base_path / f'{trimestre}_{name_shapefile}'

    return Path(shapefile_path)
