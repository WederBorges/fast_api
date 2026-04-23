import pytest  # arquivo de configuração dos testes
from fastapi.testclient import TestClient

from fast_api_zero.app import app  # importando a var app.


@pytest.fixture
def client():
    return TestClient(app)
