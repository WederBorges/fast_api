from contextlib import contextmanager
from datetime import datetime

import pytest  # arquivo de configuração dos testes
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_api_zero.app import app  # importando a var app.
from fast_api_zero.models import User, table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():

    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _moc_db_time(*, model, time=datetime(2025, 5, 26)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'created_at'):
            target.update_at = time

    event.listen(User, 'before_insert', fake_time_hook)

    yield time

    event.remove(User, 'before_inser', fake_time_hook)


@pytest.fixture
def moc_db_time():
    return _moc_db_time
