import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ads.models import User
from tests.factories import UserFactory, SelectionFactory, AdFactory, CategoryFactory

register(SelectionFactory)
register(UserFactory)
register(AdFactory)
register(CategoryFactory)

@pytest.fixture
def api_client(db):
    user = User.objects.create_user(
        first_name='john',
        last_name='test',
        username='johny',
        email='jh@test.ru',
        password='12312',

    )
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client
