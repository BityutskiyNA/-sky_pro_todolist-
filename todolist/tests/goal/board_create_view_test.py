import datetime

import pytest
from freezegun import freeze_time


@freeze_time("2023-03-10 03:21:34", tz_offset=-4)
@pytest.mark.django_db
def test_board_cr(client_auth):
    data = {
        "title": 'Test_board'
    }
    expected_response = {
        "id": 1,
        "created": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "updated": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "title": "Test_board",
        "is_deleted": False
    }

    response = client_auth.post('/goals/board/create', data=data, format='json')

    assert response.status_code == 201
    assert response.data == expected_response
