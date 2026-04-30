from contextlib import contextmanager
from datetime import datetime

import pytest  # arquivo de configuração dos testes
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api_zero.app import app  # importando a var app.
from fast_api_zero.database import get_session
from fast_api_zero.models import User, table_registry


@pytest.fixture
def user_test(session):

    user = User(username='test', email='test@example.com', password='secret')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():

    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _moc_db_time(*, model, time=datetime(2025, 5, 26)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'update_at'):
            target.update_at = time

    event.listen(User, 'before_insert', fake_time_hook)

    yield time

    event.remove(User, 'before_insert', fake_time_hook)


@pytest.fixture
def moc_db_time():
    return _moc_db_time
