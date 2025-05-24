import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_route(client):
    response = client.post('/add', data={'a': '2', 'b': '3'})
    assert b'Result: 5' in response.data

def test_subtract_route(client):
    response = client.post('/subtract', data={'a': '5', 'b': '3'})
    assert b'Result: 2' in response.data 
