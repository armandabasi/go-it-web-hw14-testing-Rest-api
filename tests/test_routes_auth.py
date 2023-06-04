from unittest.mock import MagicMock

from src.database.models import User
from src.services.auth import auth_service
from src.services.generate_password import generate_password


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user, )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user.get("email")
    assert "id" in data


def test_repeat_create_user(client, user):
    response = client.post("/api/auth/signup", json=user, )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    response = client.post("/api/auth/login", data={"username": user.get('email'), "password": user.get('password')}, )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_user(client, session, user):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get('email'), "password": user.get('password')}, )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    response = client.post("/api/auth/login", data={"username": user.get('email'), "password": "password"}, )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client, user):
    response = client.post("/api/auth/login",
                           data={"username": "email@example.com", "password": user.get('password')}, )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


def test_refresh_token(client, session, user):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    headers = {'Authorization': f'Bearer {current_user.refresh_token}'}
    response = client.get('api/auth/refresh_token', headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['token_type'] == 'bearer'


def test_confirmed_email(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = False
    session.commit()
    email_token = auth_service.create_email_token({'sub': user.get('email')})
    response = client.get(f'/api/auth/confirmed_email/{email_token}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Email confirmed'


def test_already_confirmed_email(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    email_token = auth_service.create_email_token({'sub': user.get('email')})
    response = client.get(f'/api/auth/confirmed_email/{email_token}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Your email is already confirmed'


def test_no_user_confirmed_email(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = False
    session.commit()
    email_token = auth_service.create_email_token({'sub': 'token'})
    response = client.get(f'/api/auth/confirmed_email/{email_token}')
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Verification error'


def test_request_email(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr('src.routes.auth.send_email', mock_send_email)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = False
    session.commit()
    response = client.post('/api/auth/request_email', json=user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Check your email for confirmation.'


def test_confirmation_request_email(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr('src.routes.auth.send_email', mock_send_email)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post('/api/auth/request_email', json=user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == 'Your email is already confirmed'


def test_reset_password(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr('src.routes.auth.send_email_with_password', mock_send_email)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post('/api/auth/reset_password', json=user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == "You new password send to your email."

