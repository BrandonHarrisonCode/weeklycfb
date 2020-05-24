import os
import requests
import json
import boto3


sqs = boto3.client("sqs")


def compute_week(event, context):
    if not all(key in event for key in ("year", "week")):
        print("Bad request: {}".format(event))
        return abort("Bad Request", 400)

    year = int(event["year"])
    week = int(event["week"])
    url = os.environ["APIUrl"].format(year, week)
    try:
        games = get_games(url)
    except IOError as e:
        print(e)
        return abort("Could not access the api at {}".format(url), 500)
    except ValueError as e:
        print(e)
        return abort(
            "No college football games during Year {} and Week {}.".format(year, week),
            400,
        )

    if event.get("dryrun") == True:
        print("Run is dry run, aborting message to queue.")
        return {"statusCode": 200}

    try:
        push_messages(year, week, games)
    except IOError as e:
        print(e)
        return abort(500)

    return {"statusCode": 200}


def abort(message, code):
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(message),
    }


def get_games(url):
    result = requests.get(url)
    if not result.ok:
        raise IOError("Could not access API with URL: {}".format(url))
    data = json.loads(result.content)
    if not data:
        raise ValueError("No games found with URL: {}".format(url))
    games = []
    for game in data:
        games.append(
            {
                "season": game["season"],
                "week": game["week"],
                "home_team": game["home_team"],
                "away_team": game["away_team"],
                "home_points": game["home_points"],
                "away_points": game["away_points"],
            }
        )
    return games


def push_messages(year, week, games):
    for game in games:
        print("Pushing year {} week {} to queue with data: {}".format(year, week, game))
        response = sqs.send_message(
            QueueUrl=os.environ["QueueUrl"], MessageBody=json.dumps(game),
        )
        if not response:
            raise IOError("Could not create a message for {}".format(game))
