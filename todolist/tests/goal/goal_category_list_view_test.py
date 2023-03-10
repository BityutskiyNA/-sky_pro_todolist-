import pytest
from freezegun import freeze_time

from goals.serializers import GoalCategorySerializer


@freeze_time("2023-03-10 03:21:34", tz_offset=-4)
@pytest.mark.django_db
def test_goal_category_list(client_api, board_factory, user, goal_category_factory):
    board = board_factory.create(with_owner=user)

    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)

    expected_response = [
        GoalCategorySerializer(goal_category).data
    ]
    client_api.force_login(user)
    response = client_api.get('/goals/goal_category/list')

    assert response.status_code == 200
    assert response.data == expected_response
