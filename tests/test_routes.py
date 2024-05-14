import pytest
import random
from faker import Faker
from tests.conftest import logger

fake = Faker()


def test_index(client):
    logger.info("INDEX")
    response = client.get('/')
    assert response.status_code == 200


def test_register(client):
    logger.info("REGISTER")

    test_user_data = {
        "email": "test@example.com",
        "password": "Password123!",
    }
    response = client.post('/register', json=test_user_data)
    assert response.status_code == 200

    response_data = response.json
    assert "access_token" in response_data
    assert response_data["access_token"]


@pytest.fixture
def login(client):
    logger.info("LOGIN")

    test_user_data = {
        "email": "test@example.com",
        "password": "Password123!",
    }
    response = client.post('/login', json=test_user_data)
    assert response.status_code == 200

    response_data = response.json
    assert "access_token" in response_data
    assert response_data["access_token"]

    return {
        'Authorization': f'Bearer {response_data["access_token"]}'
    }


def test_edit_profile(client, login):
    logger.info("EDIT PROFILE")

    test_profile_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "app_language": random.choice(['English', 'Spanish'])
    }

    response = client.patch('/profile', headers=login, json=test_profile_data)
    assert response.status_code == 200

    response = client.patch('/profile', headers=login, json={"app_language": "Wrong"})
    assert response.status_code == 400


def test_get_profile(client, login):
    logger.info("GET PROFILE")

    response = client.get('/profile', headers=login)
    assert response.status_code == 200

    response_data = response.json
    assert "full_name" in response_data
    assert "app_language" in response_data
    assert response_data["full_name"]
    assert response_data["app_language"]


def test_users_list_for_moderator(client, access_headers):
    logger.info("USERS LIST (MODERATOR TOKEN)")
    response = client.get('/users', headers=access_headers)
    assert response.status_code == 200


def test_users_list_for_user(client, login):
    logger.info("USERS LIST (USER TOKEN)")
    response = client.get('/users', headers=login)
    assert response.status_code == 403


def test_logout(client, login):
    logger.info("LOGOUT")
    response = client.post('/logout', headers=login)
    assert response.status_code == 200

    check = client.get('/profile', headers=login)
    assert check.status_code == 401


def test_delete_profile(client, login):
    logger.info("DELETE PROFILE")
    response = client.delete('/profile', headers=login)
    assert response.status_code == 200

    check = client.get('/profile', headers=login)
    assert check.status_code == 401
