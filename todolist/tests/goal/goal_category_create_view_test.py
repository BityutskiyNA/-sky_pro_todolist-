import datetime

import pytest
from freezegun import freeze_time


@freeze_time("2023-03-10 03:21:34", tz_offset=-4)
@pytest.mark.django_db
def test_goal_category_cr(client_auth, board):
    data = {
        "title": "test_goal_category",
        "is_deleted": False,
        "board": board.id
    }
    expected_response = {
        "id": 5,
        "created": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "updated": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "title": "test_goal_category",
        "is_deleted": False,
        "board": board.id
    }
    response = client_auth.post('/goals/goal_category/create', data=data, format='json')

    assert response.status_code == 201
    assert response.data == expected_response
