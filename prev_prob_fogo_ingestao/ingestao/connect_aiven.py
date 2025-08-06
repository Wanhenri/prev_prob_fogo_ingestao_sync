import psycopg2


def main():
    conn = psycopg2.connect(
        'postgresql://avnadmin:********@pg-1dce562c-wanhenri01-103a.d.aivencloud.com:12121/******?sslmode=require'
    )
    cur = conn.cursor()
    """
    cur.execute('CREATE SCHEMA IF NOT EXISTS previsao;')
    conn.commit()
    """

    # Cria a extensão PostGIS
    cur.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    conn.commit()

    # Verifica se foi instalada com sucesso
    cur.execute('SELECT postgis_version();')
    version = cur.fetchone()[0]
    print(f'PostGIS instalada com sucesso. Versão: {version}')

    # Limpeza
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
