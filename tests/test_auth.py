from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


# Raise Test ##################################################################


def test_token_user_not_found(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'emailnotfound@test.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_password_incorrect(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'TestePassworkIncorrect',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
