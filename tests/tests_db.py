from dataclasses import asdict

from sqlalchemy import select

from fast_api_zero.models import User


def test_create_user(session, moc_db_time):

    with moc_db_time(model=User) as time:
        new_user = User(
            username='teste', email='teste@example.com', password='secret'
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'teste'))

        assert asdict(user) == {
            'id': 1,
            'username': 'teste',
            'email': 'teste',
            'password': 'secret',
            'created_at': time,
            'update_at': time,
        }
