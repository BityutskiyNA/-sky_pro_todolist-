import pytest

from goals.serializers import BoardCreateSerializer


@pytest.mark.django_db
def test_board_list(client, client_auth, board_factory, user):
    board = board_factory.create(with_owner=user)
    expected_response = [
              BoardCreateSerializer(board).data
    ]

    response = client_auth.get('/goals/board/list')

    assert response.status_code == 200
    assert response.data == expected_response
