import pytest
import json

import access_module


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


def test_missing_yearweek(monkeypatch):
    monkeypatch.setenv('CalculatedScoresTableName', 'CalculatedScores')
    no_week_event = {'queryStringParameters': {'year': '2019'}}
    no_year_event = {'queryStringParameters': {'week': '3'}}
    no_query_event = {}
    events = [no_week_event, no_year_event, no_query_event]
    responses = [access_module.handle_access(event, None) for event in events]
    for response in responses:
        assert response
        assert 400 <= response['statusCode'] < 500
        assert response['body']
