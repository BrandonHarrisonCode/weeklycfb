import os
import json
import boto3
import decimal
import collections

from boto3.dynamodb.conditions import Key, Attr

""" Helper class to convert a DynamoDB item to JSON. """


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class Database:
    def __init__(self):
        self._database = self._get_database()

    def _get_database(self):
        calculated_scores_table_name = os.environ["CalculatedScoresTableName"]
        dynamodb = boto3.resource("dynamodb")
        database = dynamodb.Table(calculated_scores_table_name)
        database.load()

        return database

    def test(self):
        yearweeks = collections.defaultdict(set)
        response = self._database.scan(
            IndexName="YearWeek-Index",
            ExpressionAttributeNames={"#yearweek": "year:week"},
            ProjectionExpression="#yearweek",
            Select="SPECIFIC_ATTRIBUTES",
        )

        while True:
            print("DynamoDB response: {}".format(response))

            for item in response["Items"]:
                yearweek = item["year:week"]
                year = item["year:week"][: yearweek.index(":")]
                week = item["year:week"][yearweek.index(":") + 1 :]
                yearweeks[year].add(week)

            if "LastEvaluatedKey" not in response:
                break
            response = self._database.scan(
                IndexName="YearWeek-Index",
                ExpressionAttributeNames={"#yearweek": "year:week"},
                ProjectionExpression="#yearweek",
                Select="SPECIFIC_ATTRIBUTES",
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )

        return {key: list(value) for key, value in yearweeks.items()}
