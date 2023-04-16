import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_word():
    response = client.post(
        "/translate_word",
        json={
            "word": "hello",
            "lang": "es"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "hello"
    assert response.json()["translation"] == "hola"
        
def test_show_word():
    response = client.get("/world")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
        
def test_delete_word():
    response = client.post(
        "/translate_word",
        json={
            "word": "goodbye",
            "lang": "es"
        }
    )
    response = client.delete("/goodbye")
    assert response.status_code == 204
    
    response = client.get("/goodbye")
    assert response.status_code == 404