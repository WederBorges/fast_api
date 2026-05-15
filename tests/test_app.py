from http import HTTPStatus

from fast_api_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)

    -A: Arrange
    -A: Act
    -A: Assert
    """

    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}
    assert response.status_code == HTTPStatus.OK  # (200)


def test_html(client):

    response = client.get('/html')

    assert response.text == """<body> Olá mundo ! </body>"""


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'weder',
            'email': 'wilder@example.com',
            'senha': 'secret',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'weder',
        'email': 'wilder@example.com',
        'id': 1,
    }


def test_read_user_with_user(client, user_test, token):

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    users = UserPublic.model_validate(user_test).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [users]}


def test_read_user(client, token):

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'test', 'email': 'test@example.com', 'id': 1}]
    }


def test_read_user_only(client, user_test):

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user_test.username,
        'email': user_test.email,
        'id': user_test.id,
    }


def test_uptade_user(client, user_test, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'weder',
            'email': 'wilder@example.com',
            'senha': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'weder',
        'email': 'wilder@example.com',
        'id': 1,
    }


def test_delete_user(client, user_test, token):

    response = client.delete(
        f'/users/{user_test.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário EXCLUIDO'}


def test_user_only_raise_error(client, user_test):

    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_error(client, user_test, token):

    client.post(
        '/users',
        json={
            'username': '1weder',
            'email': 'wilderziioss@gmail.com',
            'senha': 'calirbe',
        },
    )

    response = client.put(
        f'/users/{user_test.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': '1weder',
            'email': 'test@example.com',
            'senha': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_get_token(client, user_test):
    response = client.post(
        '/token',
        data={'username': user_test.email, 'password': 'secret'},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'acess_token' in token
    print(token)
    print(response)
