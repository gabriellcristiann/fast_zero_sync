from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_wrong_sub_current_user(client, user):
    token_sub_not_found = create_access_token(data_payload={'sub': ''})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_sub_not_found}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_wrong_current_user(client, user):
    token_wrong_email = create_access_token(
        data_payload={'sub': 'wrong@wrong.com'}
    )

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_wrong_email}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
