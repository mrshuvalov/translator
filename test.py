import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

@pytest.mark.asyncio
async def test_create_word():
    response = await client.post(
        "/translate_word",
        json={"word": "some_word", "lang": "some_language"}
    )
    assert response.status_code == 201
    assert "word" in response.json()
    assert "translation" in response.json()

@pytest.mark.asyncio
async def test_create_word_with_invalid_word_and_lang():
    response = await client.post(
        "/translate_word",
        json={"word": "fake_word", "lang": "fake_lang"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No translation found. Please, check word and language"}

@pytest.mark.asyncio
async def test_show_word():
    response = await client.get("/some_word")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_show_word_with_invalid_word():
    response = await client.get("/fake_word")
    assert response.status_code == 404
    assert response.json() == {"detail": "Word fake_word not found"}

@pytest.mark.asyncio
async def test_delete_word():
    response = await client.delete("/some_word")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_word_with_invalid_word():
    response = await client.delete("/fake_word")
    assert response.status_code == 404
    assert response.json() == {"detail": "Word fake_word not found"}