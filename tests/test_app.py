from http import HTTPStatus


def test_root_return(client):
    """
    Este teste deve validar status_code 'OK' e
    a mensagem 'Hello World'.
    """
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
