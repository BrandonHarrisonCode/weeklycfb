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
	# Remove play by play score data from the response.
	filtered_response = [{key:game_dict[key] for key in game_dict if key != 'play-by-play'} for game_dict in response['Items']]
	return {
      'statusCode': 200,
      'headers': {},
      'body': "Required body for api gateway.",
      'data': filtered_response    
    }
