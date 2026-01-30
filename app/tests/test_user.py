import pytest
from fastapi.testclient import TestClient

def test_create_user(client):
    payload = {
        "firstName": "John",
        "lastName": "Smith",
        "email": "John.Smith@example.com",
        "password": "12345"
    }

    response = client.post("/api/user/createUser", json=payload)
    assert response.status_code == 200


def test_pretected_route_requires_auth(client):
    response = client.get("/api/user/me")
    assert response.status_code == 401
