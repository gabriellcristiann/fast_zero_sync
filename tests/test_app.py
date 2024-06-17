from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_return():
    """Este teste deve retornar Um 'ok' e Hello World"""
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
