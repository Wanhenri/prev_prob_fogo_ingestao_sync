from http import HTTPStatus

from fastapi.testclient import TestClient

from prev_prob_fogo_ingestao.app import app

Client = TestClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (Organizacao)

    response = client.get('/')  # Act( Agir )

    assert response.status_code == HTTPStatus.OK  # assert
