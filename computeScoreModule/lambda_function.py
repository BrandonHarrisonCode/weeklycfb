import os
import requests
import json
import boto3
from computescore import compute_score
from operator import itemgetter
from decimal import Decimal

calculated_scores_table_name = os.environ['CalculatedScoresTableName']
dynamodb = boto3.resource('dynamodb')
calculated_score_table = dynamodb.Table(calculated_scores_table_name)


def lambda_handler(event, context):
    print('Recieved event: {}'.format(json.dumps(event, indent=2)))
    records = event['Records']
    if len(records) > 1:
        return abort(400)
    for record in event['Records']:
        game = json.loads(str(record["body"]))

    print('Game: {}'.format(game))
    score = get_and_save_score(game)
    print('Score: {}'.format(score))

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
    calculated_score_table.put_item(
        Item={
            'year:week': '{}:{}'.format(game['season'], game['week']),
            'score': Decimal(str(score)),
            'away': game['away_team'],
            'home': game['home_team'],
            'play-by-play': list(map(lambda x: Decimal(str(x)), play_by_play)),
        }
    )
