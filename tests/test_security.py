from http import HTTPStatus

from jwt import decode

from fast_api_zero.security import ALGORITHM, SECRET_KEY, create_acess_token


def test_jwt():

    data = {'test': 'test'}

    token = create_acess_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert data['test'] == decoded['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):

    response = client.delete(
        'users/1', headers={'Authorization': 'Bearear token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}
