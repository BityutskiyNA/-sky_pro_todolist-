import pytest
from rest_framework.test import APIClient

pytest_plugins = "factories"


@pytest.fixture()
def client_api() -> APIClient:
    return APIClient()


@pytest.fixture()
def client_auth(client_api, user) -> APIClient:
    client_api.force_login(user)
    return client_api
