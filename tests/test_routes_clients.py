from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from src.database.models import User
from src.services.auth import auth_service

CLIENT = {
    "firstname": "Ivan",
    "lastname": "Ivanov",
    "email": "mark_twen@example.com",
    "phone_number": "+380501112233",
    "birthday": "1990-08-19",
    "additional_data": "some text",
}


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    current_user.role = "admin"
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_client(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.post("api/clients", json=CLIENT, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 201, response.text
        data = response.json()
        assert 'id' in data
        assert CLIENT["firstname"] == data["firstname"]


def test_create_client_second_time_email(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.post("api/clients", json=CLIENT, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 409, response.text
        data = response.json()
        assert data["detail"] == "Client with this email already exist"


def test_create_client_second_time_phone(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        client_second = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "email": "mark1_twen@example.com",
            "phone_number": "+380501112233",
            "birthday": "1990-08-19",
            "additional_data": "some text",
        }
        response = client.post("api/clients", json=client_second, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 409, response.text
        data = response.json()
        assert data["detail"] == "Client with this phone already exist"


def test_search_clients(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        params = "ivan"
        response = client.get(f"api/clients/search/?data={params}", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert CLIENT["firstname"] == data[0]["firstname"]


def test_get_clients(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("api/clients", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert 'id' in data[0]
        assert CLIENT["firstname"] == data[0]["firstname"]


def test_get_clients_by_id(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        client_id = 1
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get(f"api/clients/{client_id}", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert 'id' in data
        assert CLIENT["firstname"] == data["firstname"]


def test_get_clients_by_id_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("api/clients/1000000", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Client not found"


def test_update_client(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        client_id = 1
        updated_client = {
            "firstname": "Pavlo",
            "lastname": "Pavlov",
            "email": "mark_twen@example.com",
            "phone_number": "+380501112200",
            "birthday": "1990-08-18",
            "additional_data": "some text 2",
        }
        response = client.put(f"api/clients/{client_id}", json=updated_client,
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert 'id' in data
        assert data["id"] == client_id
        assert "firstname" in data
        assert data["firstname"] == updated_client["firstname"]
        assert data["email"] == updated_client["email"]


def test_update_client_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        updated_client = {
            "firstname": "Pavlo",
            "lastname": "Pavlov",
            "email": "mark_twen@example.com",
            "phone_number": "+380501112200",
            "birthday": "1990-08-18",
            "additional_data": "some text 2",
        }
        response = client.put("api/clients/1000000", json=updated_client,
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Client not found"


def test_get_birthday(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("api/clients/birthday/", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)


def test_remove_client(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        client_id = 1
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.delete(f"api/clients/{client_id}", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert 'id' in data
        assert data["id"] == client_id


def test_remove_client_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.delete("api/clients/100000", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Client not found"
