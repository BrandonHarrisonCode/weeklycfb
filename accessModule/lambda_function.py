import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CalculatedScores')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

"""
This function returns a list of the games for a given season and week.
"""
def lambda_handler(event, context):
	# This call should be coming from an AWS API-Gateway. Might want to find some way to check for this and fail otherwise.
  yearweek = event['queryStringParameters']['year'] + ":" + event['queryStringParameters']['week']
  response = table.query(
      KeyConditionExpression=Key('year:week').eq(yearweek)
	)
	# Remove play by play score data from the response.
  filtered_response = [{key:game_dict[key] for key in game_dict if key != 'play-by-play'} for game_dict in response['Items']]
  return {
    'isBase64Encoded': False,
      'statusCode': 200,
      'headers': {},
      'body': json.dumps(filtered_response, cls=DecimalEncoder)  
  }
