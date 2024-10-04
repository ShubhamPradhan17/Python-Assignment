import pytest
from tests.conftest import app
from flask_jwt_extended import create_access_token
import json

@pytest.fixture
def librarian_token(client):

    librarian_data = {
        'email': 'admin@example.com', 
        'password': 'Password123'
    }

    response = client.post('http://localhost:5000/login', json=librarian_data)
    
    token = response.json['token']
    return token

def test_create_member(client, librarian_token):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'phone': '1234567890',
        'address': '123 Street',
        'debt': 0.0,
        'password': 'password123'
    }
    
    headers = {
        'Authorization': f'Bearer {librarian_token}'
    }
    
    response = client.post('/create_member', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Member created successfully!'


def test_create_member_invalid_data(client, librarian_token):
    data = {
        'first_name': 'John',
        'email': 'invalid-email'
    }

    headers = {
        'Authorization': f'Bearer {librarian_token}'
    }

    response = client.post('/create_member', json=data, headers=headers)
    assert response.status_code == 400
    assert 'msg' in response.json


def test_get_members(client, librarian_token):
    headers = {
        'Authorization': f'Bearer {librarian_token}'
    }
    response = client.get('/get_member', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_members_pagination(client, librarian_token):
    headers = {
        'Authorization': f'Bearer {librarian_token}'
    }
    response = client.get('/get_member?page=1&per_page=2', headers=headers)
    assert response.status_code == 200
    assert len(response.json) <= 2
