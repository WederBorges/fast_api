from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_zero.app import app  # importando a var app.

client = TestClient(app)


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)

    -A: Arrange
    -A: Act
    -A: Assert
    """
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}
    assert response.status_code == HTTPStatus.OK  # (200)
