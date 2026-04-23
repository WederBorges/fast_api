from http import HTTPStatus


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


def teste_html(client):

    client
    response = client.get('/html')

    assert response.text == """<body> Olá mundo ! </body>"""


def teste_create_user(client):

    client

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


def test_read_user(client):

    client

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'weder',
                'email': 'wilder@example.com',
                'id': 1,
            }
        ]
    }


def test_read_user_only(client):

    client

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'weder',
        'email': 'wilder@example.com',
        'id': 1,
    }


def test_uptade_user(client):

    response = client.put(
        '/users/1?new_email=weder_gatinho@gmail.com',
        json={
            'username': 'weder',
            'email': 'wilder@example.com',
            'senha': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'weder',
        'email': 'weder_gatinho@gmail.com',
        'id': 1,
    }


def test_update_user_raise_error(client):

    response = client.put(
        '/users/2?new_email=weder_gatinho@gmail.com',
        json={
            'username': 'weder',
            'email': 'wilder@example.com',
            'senha': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):

    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'weder',
        'email': 'weder_gatinho@gmail.com',
        'id': 1,
    }


def test_delete_user_raise_error(client):

    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_only_raise_error(client):

    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
