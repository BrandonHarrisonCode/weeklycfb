import requests
import json
import boto3
from computescore import compute_score
from operator import itemgetter
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
computed_score_table = dynamodb.Table('CalculatedScores')


def lambda_handler(event, context):
    records = event['Records']
    if len(records) > 1:
        return abort(400)
    for record in event['Records']:
       game = json.loads(str(record["body"]))

    score = get_and_save_score(game)
    print(score)

    return {
        'statusCode': 200
    }


def abort(statuscode):
    return {
        'statusCode': statuscode
    }

def get_and_save_score(game):
    title = '{} vs. {}'.format(game['home_team'], game['away_team'])
    print(title)
    score, play_by_play = compute_score(game)
    print('Final score: {}\n\n'.format(score))
    output = {'title': title, 'score': score}
    store_score(game, score, play_by_play)
    return output


def store_score(game, score, play_by_play):
    computed_score_table.put_item(
        Item={
            'year:week': '{}:{}'.format(game['season'], game['week']),
            'score': Decimal(str(score)),
            'away': game['away_team'],
            'home': game['home_team'],
            'play-by-play': list(map(lambda x: Decimal(str(x)), play_by_play)),
        }
    )
