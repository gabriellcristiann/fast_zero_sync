from http import HTTPStatus
from fastapi import HTTPExceptions
from jwt import decode
import pytest

from fast_zero.security import create_access_token, settings, get_current_user


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


def test_get_current_user_error():
    with pytest.raises(HTTPExceptions):
        get_current_user({''})
