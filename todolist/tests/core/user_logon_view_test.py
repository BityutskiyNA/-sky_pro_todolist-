import pytest


@pytest.mark.django_db()
class TestLoginView:
    url = reversed('core:login')

    def test_user_not_found(self, client, user_factory):
        user = user_factory.build()
        data = {
            "username": user.username,
            "password": user.password
        }
        response = client.post(self.url, data=data)

        assert response.status_code == 404

    def test_user_create(self, client):
        password = 'fjslfjaajf;ajfafj333'
        username = 'test'

        data = {
            "username": username,
            "password": password,
            "password_repeat": password
        }
        expected_response = {
            "id": 1,
            "username": username,
            "first_name": "",
            "last_name": "",
            "email": ""
        }

        response = client.post('/core/signup', data=data, format='json', )

        assert response.status_code == 201
        assert response.data == expected_response
