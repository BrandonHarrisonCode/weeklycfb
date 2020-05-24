import os
import json
import boto3
import decimal

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
        self.database = self.get_database()

    def retrieve_game(self, yearweek):
        response = self.database.query(
            IndexName="Score-Index",
            KeyConditionExpression=Key("year:week").eq(yearweek),
            ProjectionExpression="home,away,score",
            ScanIndexForward=False,
            Select="SPECIFIC_ATTRIBUTES",
            Limit=10,
        )
        built_response = {"yearweek": yearweek, "data": response["Items"]}
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(built_response, cls=DecimalEncoder),
        }

    def get_database(self):
        calculated_scores_table_name = os.environ["CalculatedScoresTableName"]
        dynamodb = boto3.resource("dynamodb")
        database = dynamodb.Table(calculated_scores_table_name)
        database.load()

        return database
