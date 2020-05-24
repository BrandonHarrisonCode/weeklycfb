import json

from database import DecimalEncoder, Database

"""
This function returns a list of the games for a given season and week.

Example input:
    event = {
      queryStringParameters:
        year: '2019'
        week: '3'
    }
"""


def handle_access(event, context):
    if not "queryStringParameters" in event or not all(
        key in event["queryStringParameters"] for key in ("year", "week")
    ):
        print("Bad request: {}".format(event))
        return abort("Bad Request", 400)

    yearweek = (
        str(event["queryStringParameters"]["year"])
        + ":"
        + str(event["queryStringParameters"]["week"])
    )
    return Database().retrieve_game(yearweek)


def abort(message, code):
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(message, cls=DecimalEncoder),
    }
