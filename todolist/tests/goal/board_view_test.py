import pytest

from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_board_get_by_id(client_auth, board_factory, user):
    board = board_factory.create(with_owner=user)
    response = client_auth.get(f'/goals/board/{board.id}')

    assert response.status_code == 200
    assert response.data == BoardSerializer(board).data


@pytest.mark.django_db
def test_board_delete_by_id(client_api, board_factory, user):
    board = board_factory.create(with_owner=user)
    client_api.force_login(user)
    response = client_api.delete(f'/goals/board/{board.id}')

    assert response.status_code == 204
