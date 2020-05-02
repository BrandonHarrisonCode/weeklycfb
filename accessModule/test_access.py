import pytest
import json

import access_module
import database


def test_valid_yearweek(monkeypatch):
    monkeypatch.setenv('CalculatedScoresTableName', 'CalculatedScores')
    event = {'queryStringParameters': {'year': '2019', 'week': '3'}}
    response = access_module.handle_access(event, None)
    print(response)
    assert response
    assert 200 <= response['statusCode'] < 300
    assert response['body']
    assert json.loads(response['body'])['data']


def test_invalid_yearweek(monkeypatch):
    monkeypatch.setenv('CalculatedScoresTableName', 'CalculatedScores')
    event = {'queryStringParameters': {'year': '2019', 'week': '23'}}
    response = access_module.handle_access(event, None)
    print(response)
    assert response
    assert 200 <= response['statusCode'] < 300
    assert response['body']
    assert len(json.loads(response['body'])['data']) == 0
