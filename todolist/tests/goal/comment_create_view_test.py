import datetime

import pytest
from freezegun import freeze_time


@freeze_time("2023-03-10 03:21:34", tz_offset=-4)
@pytest.mark.django_db
def test_goal_comment_cr(client_api, board_factory, goal_category_factory, user, goal_factory):

    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)
    goal = goal_factory(category=goal_category, user=user)

    data = {
        "text": "Комментарий для теста",
        "goal": goal.id
    }
    expected_response = {
        "id": 1,
        "created": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "updated": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "text": "Комментарий для теста",
        "goal": goal.id
    }

    client_api.force_login(user)
    response = client_api.post('/goals/goal_comment/create', data=data, format='json')

    assert response.status_code == 201
    assert response.data == expected_response
