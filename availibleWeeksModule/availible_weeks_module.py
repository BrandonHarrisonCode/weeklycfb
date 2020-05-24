import boto3
import json

from database import DecimalEncoder, Database


def retrieve_years_and_weeks():
    test = Database()
    yearweeks = test.test()
    built_response = {"data": yearweeks}
    print(built_response)

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(built_response, cls=DecimalEncoder),
    }


def handle_request(event, context):
    # This call should be coming from an AWS API-Gateway. Might want to find some way to check for this and fail otherwise.
    print("Recieved request.")
    return retrieve_years_and_weeks()


def abort(message, code):
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(message, cls=DecimalEncoder),
    }
