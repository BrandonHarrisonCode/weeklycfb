import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CalculatedScores')

"""
This function returns a list of the games for a given season and week.
"""
def lambda_handler(event, context):
	response = table.query(
    KeyConditionExpression=Key('year:week').eq("2018:13")
	)
	return {
      'statusCode': 200,
      'data': response['Items']
  }
