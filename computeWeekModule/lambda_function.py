import os
import requests
import json
import boto3

sqs = boto3.client('sqs')
queue_url = os.environ['QueueUrl']


def lambda_handler(event, context):
    year = int(event['year'])
    week = int(event['week'])
    base = 'https://api.collegefootballdata.com/games?seasonType=both&year={}&week={}'
    url = base.format(year, week)
    try:
        games = get_games(url)
    except IOError as e:
        print(e)
        return abort(500)
    except ValueError as e:
        print(e)
        return abort(400)

    try:
        push_messages(year, week, games)
    except IOError as e:
        print(e)
        return abort(500)

    return {
        'statusCode': 200
    }


def abort(statuscode):
    return {
        'statusCode': statuscode
    }


def get_games(url):
    result = requests.get(url)
    if not result.ok:
        raise IOError('Could not access API with URL: {}'.format(url))
    data = json.loads(result.content)
    if not data:
        raise ValueError('No games found with URL: {}'.format(url))
    games = []
    for game in data:
        games.append({
            'season': game['season'],
            'week': game['week'],
            'home_team': game['home_team'],
            'away_team': game['away_team'],
            'home_points': game['home_points'],
            'away_points': game['away_points'],
        })
    return games


def push_messages(year, week, games):
    for game in games:
        print('Pushing year {} week {} to queue with data: {}'.format(year, week, game))
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(game),
        )
        if not response:
            raise IOError('Could not create a message for {}'.format(game))
