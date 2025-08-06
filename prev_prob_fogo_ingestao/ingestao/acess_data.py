import psycopg2
from dotenv import load_dotenv


def main():
    # Carrega variáveis do arquivo .env
    load_dotenv()

    # Substitua com sua URL real (atenção ao sslmode=require)
    conn = psycopg2.connect(
        'postgresql://avnadmin:********@pg-1dce562c-wanhenri01-103a.d.aivencloud.com:12121/*******?sslmode=require'
    )

    cur = conn.cursor()

    '''
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'previsao' AND table_name = 'previsao_2025';
    """)
    '''
    cur.execute("""
        SELECT
            "CD_MUN",
            "NM_MUN_y",
            "SIGLA_UF",
            "AREA_KM2",
            "Sum_Frs",
            alerta,
            fc_2021,
            fc_2022,
            fc_2023,
            fc_2024,
            "Trend",
            "Secas",
            prev_t,
            prev_p,
            regra,
            ano,
            trimestre
        FROM previsao.previsao_2025
        WHERE trimestre = 'ASO'
        ORDER BY "SIGLA_UF", "CD_MUN"
        LIMIT 5;
    """)

    trimestres = cur.fetchall()

    print('Trimestres existentes:')
    for trimestre in trimestres:
        print(trimestre[0])

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
