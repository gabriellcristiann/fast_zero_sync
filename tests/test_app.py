from http import HTTPStatus


def test_root_return(client):
    """
    Este teste deve validar status_code 'OK' e
    a mensagem 'Hello World'
    """

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


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

    # Validar status code correto
    assert response.status_code == HTTPStatus.CREATED

    # Validar UserPublic
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

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }


def test_get_user(client):
    """
    Este teste deve validar o status_code 'OK' e
    o retorno de um usuário.
    """

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_update_user(client):
    """
    Este teste deve validar o status_code 'OK' e
    a atualização de dados do usuário.
    """

    response = client.put(
        '/users/1',
        json={
            'username': 'testupdatename',
            'email': 'testupdatemail@test.com',
            'password': 'test_pass',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testupdatename',
        'email': 'testupdatemail@test.com',
        'id': 1,
    }


def test_delete_user(client):
    """
    Este teste deve validar o status_code 'OK' e
    a deleção de dados do usuário.
    """

    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_user_put_not_found(client):
    """
    Este teste deve validar o status_code 'NOT FOUND' e
    a mensagem 'User not Found'
    """

    response = client.put(
        '/users/8',
        json={
            'username': 'testusernotfound',
            'email': 'test@test.com',
            'password': 'test_pass',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_user_delete_not_found(client):
    """
    Este teste deve validar o status_code 'NOT FOUND' e
    a mensagem 'User not Found'
    """

    response = client.delete(
        '/users/8',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_user_get_not_found(client):
    """
    Este teste deve validar o status_code 'NOT FOUND' e
    a mensagem 'User not Found do endpoint get_user'
    """

    response = client.get(
        '/users/8',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
