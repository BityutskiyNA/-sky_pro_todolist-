import datetime

import pytest
from freezegun import freeze_time


@freeze_time("2023-03-10 03:21:34", tz_offset=-4)
@pytest.mark.django_db
def test_goal_cr(client_api, board_factory, goal_category_factory, user):
    board = board_factory.create(with_owner=user)
    goal_category = goal_category_factory.create(title='Тестовая категория из теста', user=user, board=board)
    data = {
      "category": goal_category.id,
      "title": "string",
      "description": "string",
      "due_date": "2023-03-08",
      "status": 1,
      "priory": 1
    }

    expected_response = {
        "id": 5,
        "category": goal_category.id,
        "created": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "updated": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "title": "string",
        "description": "string",
        "status": 1,
        "priory": 1,
        "due_date": "2023-03-08"
    }

    client_api.force_login(user)
    response = client_api.post('/goals/goal/create', data=data, format='json')

    assert response.status_code == 201
    assert response.data == expected_response
