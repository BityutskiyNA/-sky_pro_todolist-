import pytest

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_goal_get_by_id(client_api, board_factory, user, goal_category_factory, goal_factory,):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)
    goal = goal_factory(category=goal_category, user=user)
    client_api.force_login(user)
    response = client_api.get(f'/goals/goal/{goal.id}')

    assert response.status_code == 200
    assert response.data == GoalSerializer(goal).data


@pytest.mark.django_db
def test_goal_delete_by_id(client_api, board_factory, user, goal_category_factory, goal_factory):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(
        title='Тестовая категория из теста',
        user=user, board=board)
    goal = goal_factory(category=goal_category, user=user)

    client_api.force_login(user)
    response = client_api.delete(f'/goals/goal/{goal.id}')

    assert response.status_code == 204
