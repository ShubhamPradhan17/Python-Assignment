import json
from tests.conftest import app

def test_get_books(client):
    response = client.get('/get_books?page=1&per_page=2')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) <= 2
    
    if len(data) > 0:
        book = data[0]
        assert "id" in book
        assert "book_name" in book
        assert "author" in book

def test_get_books_with_invalid_page(client):
    response = client.get('/get_books?page=abc&per_page=2')
    
   
    assert response.status_code == 400
    data = json.loads(response.data)

    assert 'msg' in data 


