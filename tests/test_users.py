from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    """
    Este teste deve validar o status_code 'CREATED' e
    os dados do usuário criado.
    """
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'test_pass',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_users(client):
    """
    Este teste deve validar o status_code 'OK' e
    o retorno de uma lista de usuários.
    """
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user, outher_user):
    """
    Este teste deve validar o status_code 'OK' e
    o retorno de uma lista de usuários contendo
    os dados do usuário criado.
    """
    user_schema = UserPublic.model_validate(user).model_dump()
    outrher_user_schema = UserPublic.model_validate(outher_user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema, outrher_user_schema]}


def test_get_user(client, user):
    """
    Este teste deve validar o status_code 'OK' e
    o retorno dos dados do usuário específico.
    """
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user, token):
    """
    Este teste deve validar o status_code 'OK' e
    a atualização de dados do usuário.
    """
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testuser',
            'email': 'emailtest@update.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testuser',
        'email': 'emailtest@update.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    """
    Este teste deve validar o status_code 'OK' e
    a deleção de dados do usuário.
    """
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# Raise Test ##################################################################


def test_user_get_not_found(client, user):
    """
    Este teste deve validar o status_code 'NOT FOUND' e
    a mensagem 'User not Found do endpoint get_user'.
    """
    response = client.get('/users/8')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_create_user_exits(client, user):
    """
    Este teste deve validar o status_code 'BAD REQUEST' e
    a mensagem 'Username already exists' quando o nome
    de usuário já está em uso.
    """
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_exits(client, user):
    """
    Este teste deve validar o status_code 'BAD REQUEST' e
    a mensagem 'Email already exists' quando o email
    já está em uso.
    """
    response = client.post(
        '/users/',
        json={
            'username': 'test2',
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_update_with_wrong_user(client, outher_user, token):
    """
    Este teste deve validar o status_code 'FORBIDDEN' e
    a mensagem 'Not enough permissions'
    ao tentar atualizar um usuário inexistente.
    """
    response = client.put(
        f'/users/{outher_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Teste',
            'email': 'test@test.com',
            'password': 'test_pass',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_with_wrong_user(client, outher_user, token):
    """
    Este teste deve validar o status_code 'FORBIDDEN' e
    a mensagem 'Not enough permissions'
    ao tentar deletar um usuário inexistente.
    """
    response = client.delete(
        f'/users/{outher_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
