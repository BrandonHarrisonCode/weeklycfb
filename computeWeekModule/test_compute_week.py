import pytest
import json
import requests

import compute_week_module


def test_valid_yearweek(monkeypatch):
    monkeypatch.setenv('APIUrl', 'https://api.collegefootballdata.com/games?seasonType=both&year={}&week={}')
    event = {'year': '2019', 'week': '3', 'dryrun': True}
    response = compute_week_module.compute_week(event, None)
    print(response)
    assert response
    assert 200 <= response['statusCode'] < 300


def test_invalid_yearweek(monkeypatch):
    monkeypatch.setenv('APIUrl', 'https://api.collegefootballdata.com/games?seasonType=both&year={}&week={}')
    event = {'year': '2019', 'week': '23', 'dryrun': True}
    response = compute_week_module.compute_week(event, None)
    print(response)
    assert response
    assert 400 <= response['statusCode'] < 500


def test_missing_yearweek(monkeypatch):
    monkeypatch.setenv('APIUrl', 'https://api.collegefootballdata.com/games?seasonType=both&year={}&week={}')
    no_week_event = {'year': '2019', 'dryrun': True}
    no_year_event = {'week': '3', 'dryrun': True}
    no_query_event = {}
    events = [no_week_event, no_year_event, no_query_event]
    responses = [compute_week_module.compute_week(event, None) for event in events]
    for response in responses:
        assert response
        assert 400 <= response['statusCode'] < 500


def test_inaccessable_api(monkeypatch):
    monkeypatch.setenv('APIUrl', 'https://fakeurl')

    event = {'year': '2019', 'week': '3', 'dryrun': True}
    response = compute_week_module.compute_week(event, None)
    print(response)
    assert response
    assert 500 <= response['statusCode'] < 600
