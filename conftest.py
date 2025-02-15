import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def create_user(db):
    """Фикстура для создания пользователя"""

    def make_user(id="test@example.com", password="password"):
        User = get_user_model()
        user = User.objects.create_user(id=id, password=password)
        print(f'create_user --- {user}')
        return user
    return make_user


@pytest.fixture
def api_client():
    """Фикстура для тестового клиента"""

    return APIClient()
