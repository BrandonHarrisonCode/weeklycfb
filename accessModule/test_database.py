import pytest
import json
import boto3

import database

database_client = boto3.client("dynamodb")


def test_valid_database(monkeypatch):
    monkeypatch.setenv("CalculatedScoresTableName", "CalculatedScores")
    assert database.Database()


def test_missing_database(monkeypatch):
    monkeypatch.setenv("CalculatedScoresTableName", "non_existant_database")
    with pytest.raises(database_client.exceptions.ResourceNotFoundException):
        database.Database()
