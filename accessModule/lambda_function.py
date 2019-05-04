import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CalculatedScores')
def lambda_handler(event, context):
	response = table.query(
    KeyConditionExpression=Key('year:week').eq("2018:13")
	)
	return response