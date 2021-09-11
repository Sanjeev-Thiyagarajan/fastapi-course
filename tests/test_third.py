import pytest
from jose import JWTError, jwt
from app.config import settings


def test_create_user(client):
    print("Testing client test")
    response = client.post(
        "/users", json={"email": "sanjeev@gmail.com", "password": "password123"})

    assert response.status_code == 201


def test_login_user(client, test_user):

    print("Login User")
    response = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200

    token = response.json().get("access_token")
    payload = jwt.decode(token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert response.json().get("token_type") == "bearer"

    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})

    assert response.status_code == status_code
