import pytest


@pytest.mark.django_db
def test_user_get_by_id(client_api, user_factory):
    password = 'fjslfjaajf;ajfafj333'
    username = 'test_for_api'
    user = user_factory.create(username=username, password=password, email='test@test.ru', is_superuser=True)
    client_api.force_login(user)
    response = client_api.get('/core/profile')
    expected_response = {
        # "id": user.id,
        "username": username,
        "first_name": "",
        "last_name": "",
        "email": "test@test.ru"
    }
    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_delete_by_id(client_api, user):
    client_api.force_login(user)
    response = client_api.delete('/core/profile')

    assert response.status_code == 204
