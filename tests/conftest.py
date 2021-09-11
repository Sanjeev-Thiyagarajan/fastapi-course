from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.database import Base
from app.config import settings
import pytest
from alembic import command
from alembic.config import Config
from app import models
from app.oauth2 import create_access_token


# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost:5432/fastapi-test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("drop and creat tables")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("getting db")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {
        "email": "sanjeev@gmail.com",
        "password": "password123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def test_user2(client):
    user_data = {
        "email": "sanjeev123@gmail.com",
        "password": "password123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_user(n):
        return models.Post(**n)
    user_map = map(create_user, posts_data)
    users = list(user_map)
    session.add_all(users)

    session.commit()
    posts = session.query(models.Post).all()

    return posts
