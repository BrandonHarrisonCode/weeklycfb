import os
import boto3
import json
import decimal
import collections

from boto3.dynamodb.conditions import Key, Attr

calculated_scores_table_name = os.environ['CalculatedScoresTableName']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(calculated_scores_table_name)

# Helper class to convert a DynamoDB item to JSON.


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def scanDB():
    yearweeks = collections.defaultdict(set)
    response = table.scan(
            IndexName="YearWeek-Index",
            ExpressionAttributeNames={"#yearweek": "year:week"},
            ProjectionExpression="#yearweek",
            Select="SPECIFIC_ATTRIBUTES",
            )

    while True:
        print('DynamoDB response: {}'.format(response))

        for item in response['Items']:
            yearweek = item['year:week']
            year = item['year:week'][:yearweek.index(':')]
            week = item['year:week'][yearweek.index(':') + 1:]
            yearweeks[year].add(week)

        if 'LastEvaluatedKey' not in response:
            break
        response = table.scan(
            IndexName="YearWeek-Index",
            ExpressionAttributeNames={"#yearweek": "year:week"},
            ProjectionExpression="#yearweek",
            Select="SPECIFIC_ATTRIBUTES",
            ExclusiveStartKey=response['LastEvaluatedKey']
            )

    return {key: list(value) for key, value in yearweeks.items()}


def retrieve_years_and_weeks():
    yearweeks = scanDB()
    built_response = {
        'data': yearweeks
    }
    print(built_response)

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(built_response, cls=DecimalEncoder)
    }


"""
This function returns a list of the weeks and years stored in the database.
"""


def lambda_handler(event, context):
    # This call should be coming from an AWS API-Gateway. Might want to find some way to check for this and fail otherwise.
    print('Recieved request.')
    return retrieve_years_and_weeks()


def abort(message, code):
    return {
        'isBase64Encoded': False,
        'statusCode': code,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(message, cls=DecimalEncoder)
    }
