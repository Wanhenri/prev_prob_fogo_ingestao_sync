import os
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cores suaves em tons de vermelho
ALERTA_CORES = {
    'alert': '#ffaa01',  # vermelho claro
    'attention': '#ffff00',  # vermelho médio
    'high alert': '#e60000',  # vermelho vivo
    'observation': '#89cd67',  # verde claro
    'low probability': '#01c4ff',  # azul claro
}

ALERTA_TRADUZIDO = {
    'high alert': 'Alerta Alto',
    'alert': 'Alerta',
    'attention': 'Atenção',
    'low probability': 'Baixa probabilidade',
    'observation': 'Observação',
}

COR_DEFAULT = '#CCCCCC'  # Cor cinza para valores não reconhecidos

BASE_DIR = Path('/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202507/CPTEC/')


def plotar_estados(
    gdf,
    ufs: list[str],
    column: str = 'alerta',
    title: str = 'Mapa de Alerta',
    ordem_legenda: list[str] = None,
):
    try:
        # gdf = gdf
        ...
    except Exception as e:
        print(f'❌ Erro ao carregar shapefile: {e}')
        return

    if 'sigla_uf' not in gdf.columns or column not in gdf.columns:
        print('❌ Colunas esperadas não encontradas.')
        print('Colunas disponíveis:', gdf.columns.tolist())
        return

    # Filtrar pelos estados desejados
    gdf_estados = gdf[gdf['sigla_uf'].isin(ufs)].copy()

    if gdf_estados.empty:
        print(f'⚠️ Nenhum dado encontrado para os estados: {ufs}')
        return

    # Normalizar a coluna de alerta (linha quebrada)
    gdf_estados['alerta_normalizado'] = (
        gdf_estados[column].astype(str).str.strip().str.lower()
    )

    # Atribuir cores (linha quebrada)
    gdf_estados['cor'] = (
        gdf_estados['alerta_normalizado'].map(ALERTA_CORES).fillna(COR_DEFAULT)
    )

    # --- Plotting Setup ---
    fig, ax = plt.subplots(figsize=(12, 12))
    gdf_estados.plot(
        ax=ax, color=gdf_estados['cor'], edgecolor='black', linewidth=0.5
    )
    gdf_estados_dissolved = gdf_estados.dissolve(by='sigla_uf')
    gdf_estados_dissolved.plot(
        ax=ax, facecolor='none', edgecolor='black', linewidth=2.0
    )

    ax.set_title(title, fontsize=16)
    ax.axis('off')

    # Adicionar contorno do Pantanal
    # Conexão com o banco de dados
    engine = create_engine(
        'postgresql://neondb_owner:********@ep-calm-sun-acqqs9yf-pooler.sa-east-1.aws.neon.tech/******?sslmode=require&channel_binding=require'
    )

    sql = """
        SELECT * FROM biomas.pantanal LIMIT 1;
    """

    gdf_pantanal = gpd.read_postgis(sql, con=engine, geom_col='geom')

    if not gdf_pantanal.empty:
        gdf_pantanal.boundary.plot(
            ax=ax,
            color='black',
            linewidth=2.5,
            linestyle='-',
            label='Pantanal',
        )
        exibir_pantanal = True
    else:
        print("⚠️ Bioma 'Pantanal' não encontrado no banco de dados.")
        exibir_pantanal = False

    # Legenda
    if ordem_legenda:
        categorias_legenda = [
            c
            for c in ordem_legenda
            if c in gdf_estados['alerta_normalizado'].unique()
        ]
    else:
        categorias_legenda = sorted(gdf_estados['alerta_normalizado'].unique())

    legend_patches = [
        mpatches.Patch(
            color=ALERTA_CORES.get(cat, COR_DEFAULT),
            label=ALERTA_TRADUZIDO.get(cat, cat),
        )
        for cat in categorias_legenda
    ]

    if exibir_pantanal:
        pantanal_patch = mpatches.Patch(
            facecolor='none',
            edgecolor='black',
            linestyle='-',
            linewidth=2,
            label='Pantanal',
        )
        legend_patches.append(pantanal_patch)

    ax.legend(
        handles=legend_patches, title='Nível de Alerta', loc='lower left'
    )

    # Salvar imagem
    estados_nome = '_'.join(ufs)
    output_path = BASE_DIR / f'mapa_{estados_nome}_alerta.png'
    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    print(f'✅ Mapa salvo em: {output_path}')

    plt.show()


if __name__ == '__main__':
    """
    # ufs_desejadas = [
    # "MS", "MT", "GO", "DF",
    # "RO", "AM", "PA", "TO",
    # "SP", "MG"]
    """

    ufs_desejadas = ['MS', 'MT', 'GO', 'DF']
    ordem_personalizada = [
        'high alert',
        'alert',
        'attention',
        'observation',
        'low probability',
    ]

    def carregar_dados_do_banco(ufs, ordem_legenda):

        load_dotenv()

        # Lê a URL do banco de dados
        engine_url = os.getenv('DB_URL')

        # Criar conexão
        engine = create_engine(engine_url)

        # Montar SQL com nomes de colunas corretamente entre aspas
        sql = f"""
        SELECT * FROM previsao.previsao_2025
        WHERE "SIGLA_UF" IN ({','.join(f"'{uf}'" for uf in ufs)})
        AND "trimestre" = 'JJA'
        """

        # Ler como GeoDataFrame
        gdf = gpd.read_postgis(sql, con=engine, geom_col='geometry')

        # Normaliza os nomes das colunas (tudo em minúsculas)
        gdf.columns = gdf.columns.str.lower()

        # Padroniza os valores da legenda
        gdf['alerta'] = gdf['alerta'].str.lower()

        return gdf

    # Carrega os dados diretamente do banco
    gdf = carregar_dados_do_banco(ufs_desejadas, ordem_personalizada)

    # Chama sua função original de plotagem
    plotar_estados(
        gdf=gdf,
        ufs=ufs_desejadas,
        column='alerta',
        title='Mapa de Alerta - Brasil',
        ordem_legenda=ordem_personalizada,
    )
