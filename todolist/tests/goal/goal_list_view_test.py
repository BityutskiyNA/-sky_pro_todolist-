import pytest

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_goal_list(client_api, board_factory, user, goal_category_factory, goal_factory):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)
    goal = goal_factory(category=goal_category, user=user)
    expected_response = [
        GoalSerializer(goal).data
    ]
    client_api.force_login(user)
    response = client_api.get('/goals/goal/list')

    assert response.status_code == 200
    assert response.data == expected_response
