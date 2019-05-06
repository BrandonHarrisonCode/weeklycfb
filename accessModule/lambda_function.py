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
			KeyConditionExpression=Key('year:week').eq(yearweek),
			ProjectionExpression="score,home,away",
			ScanIndexForward=False,
			Select="SPECIFIC_ATTRIBUTES"
	)
	return {
		'isBase64Encoded': False,
		'statusCode': 200,
		'headers': {            
			"Access-Control-Allow-Origin": "*"
		},
		'body': json.dumps(response['Items'], cls=DecimalEncoder)  
	}
