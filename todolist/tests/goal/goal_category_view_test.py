import pytest

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_goal_category_get_by_id(client_api, board_factory, user, goal_category_factory):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)

    client_api.force_login(user)
    response = client_api.get(f'/goals/goal_category/{goal_category.id}')

    assert response.status_code == 200
    assert response.data == GoalCategorySerializer(goal_category).data


@pytest.mark.django_db
def test_goal_category_delete_by_id(client_api, board_factory, user, goal_category_factory):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)

    client_api.force_login(user)
    response = client_api.delete(f'/goals/goal_category/{goal_category.id}')

    assert response.status_code == 204
