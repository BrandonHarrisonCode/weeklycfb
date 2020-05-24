import pytest
import json
import boto3

import availible_weeks_module
import database


database_client = boto3.client("dynamodb")


def test_smoketest(monkeypatch):
    monkeypatch.setenv("CalculatedScoresTableName", "CalculatedScores")
    response = availible_weeks_module.handle_request(None, None)
    print(response)
    assert response
    assert 200 <= response["statusCode"] < 300
    assert response["body"]
    assert json.loads(response["body"])["data"]


def test_valid_database(monkeypatch):
    monkeypatch.setenv("CalculatedScoresTableName", "CalculatedScores")
    assert database.Database()


def test_missing_database(monkeypatch):
    monkeypatch.setenv("CalculatedScoresTableName", "non_existant_database")
    with pytest.raises(database_client.exceptions.ResourceNotFoundException):
        database.Database()
