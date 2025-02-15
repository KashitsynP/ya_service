import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_user_info_view(api_client, create_user):
    """Тест на получение информации о пользователе"""

    user = create_user()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse("user-info")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == 'test@example.com'
    assert response.data['id_type'] == "email"
