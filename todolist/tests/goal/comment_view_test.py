import pytest

from goals.serializers import CommentSerializer


@pytest.mark.django_db
def test_comment_get_by_id(client_api, board_factory, user, goal_category_factory, goal_factory,
                           goal_comment_factory):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)
    goal = goal_factory(category=goal_category, user=user)
    goal_comment = goal_comment_factory.create(goal=goal, user=user)
    client_api.force_login(user)
    response = client_api.get(f'/goals/goal_comment/{goal_comment.id}')

    assert response.status_code == 200
    assert response.data == CommentSerializer(goal_comment).data


@pytest.mark.django_db
def test_comment_delete_by_id(client_api, board_factory, user, goal_category_factory, goal_factory,
                              goal_comment_factory):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)
    goal = goal_factory(category=goal_category, user=user)
    goal_comment = goal_comment_factory.create(goal=goal, user=user)

    client_api.force_login(user)
    response = client_api.delete(f'/goals/goal_comment/{goal_comment.id}')

    assert response.status_code == 204
