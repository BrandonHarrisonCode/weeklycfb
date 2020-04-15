import os
import boto3
import json
import decimal

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


def abort(message, code):
    return {
            'isBase64Encoded': False,
            'statusCode': code,
            'headers': {
                    "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(message, cls=DecimalEncoder)
    }


def retrieve_game(yearweek):
    response = table.query(
            IndexName='Score-Index'
            KeyConditionExpression=Key('year:week').eq(yearweek),
            ProjectionExpression="home,away,score",
            ScanIndexForward=False,
            Select='SPECIFIC_ATTRIBUTES',
            Limit=10
            )
    built_response = {
            'yearweek': yearweek,
            'data': response['Items']
    }
    return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {
                    "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(built_response, cls=DecimalEncoder)
    }


"""
This function returns a list of the games for a given season and week.
"""


def lambda_handler(event, context):
    # This call should be coming from an AWS API-Gateway. Might want to find some way to check for this and fail otherwise.
    if not 'queryStringParameters' in event or not all(key in event['queryStringParameters'] for key in ('year', 'week')):
        abort("Bad Request", 400)

    yearweek = event['queryStringParameters']['year'] + ":" + event['queryStringParameters']['week']
    return retrieve_game(yearweek)
