import pytest

from prev_prob_fogo_ingestao.ingestao.acessar_banco import db_engine


def test_conexao_banco_sucesso():
    """
    Testa se a conexão com o banco de dados pode ser estabelecida.
    """
    try:
        # Tenta conectar ao banco de dados usando o engine da fixture
        with db_engine().connect() as conn:
            # Se a conexão for bem-sucedida, a variável `conn` não será None.
            assert conn is not None
        print('\n✅ Conexão com o banco de dados estabelecida com sucesso.')
    except Exception as e:
        # Se ocorrer qualquer erro na conexão, o teste falha
        pytest.fail(f'❌ Falha ao conectar ao banco de dados. Erro: {e}')
