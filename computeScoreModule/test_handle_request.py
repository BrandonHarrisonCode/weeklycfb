import pytest
import json
import requests

import handle_request


def test_smoketest():
    event = {"Records": [{"body": '{"season": 2019, "week": 3, "home_team": "Northwestern", "away_team": "UNLV", "home_points": 30, "away_points": 14, "dryrun": true}'}]}
    response = handle_request.handle_request(event, None)
    print(response)
    assert response
    assert 200 <= response['statusCode'] < 300
