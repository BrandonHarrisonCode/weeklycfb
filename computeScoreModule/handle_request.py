import os
import requests
import json
import boto3
from score_calculator import compute_score
from operator import itemgetter
from decimal import Decimal


def handle_request(event, context):
    print("Recieved event: {}".format(json.dumps(event, indent=2)))
    records = event["Records"]
    if len(records) > 1:
        return abort(400)
    for record in event["Records"]:
        game = json.loads(str(record["body"]))

    print("Game: {}".format(game))
    title, score, play_by_play = get_score(game)
    print("{}: {}".format(title, score))
    print("Play by play: {}".format(play_by_play))
    # Do not save the game if the dry_run flag is present
    if game.get("dryrun"):
        print("Dry run. Not saving score")
    else:
        store_score(game, score, play_by_play)

    return {"statusCode": 200}


def abort(statuscode):
    return {"statusCode": statuscode}


def get_score(game):
    title = "{} vs. {}".format(game["home_team"], game["away_team"])
    print(title)
    score, play_by_play = compute_score(game)
    print("Final score: {}\n\n".format(score))
    return title, score, play_by_play


def store_score(game, score, play_by_play):
    dynamodb = boto3.resource("dynamodb")
    calculated_score_table = dynamodb.Table(os.environ["CalculatedScoresTableName"])
    response = calculated_score_table.update_item(
        ExpressionAttributeNames={"#pbp": "play-by-play"},
        Key={
            "year:week": "{}:{}".format(game["season"], game["week"]),
            "home": game["home_team"],
        },
        UpdateExpression="set away = :away, score = :score, #pbp = :pbp",
        ExpressionAttributeValues={
            ":away": game["away_team"],
            ":score": Decimal(str(score)),
            ":pbp": list(map(lambda x: Decimal(str(x)), play_by_play)),
        },
        ReturnValues="ALL_OLD",
    )
