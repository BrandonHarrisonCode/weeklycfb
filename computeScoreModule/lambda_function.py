import requests
import json
import boto3
from computescore import compute_score
from operator import itemgetter
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
computed_score_table = dynamodb.Table('CalculatedScores')


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

    scores = get_scores(year, week, games)
    print(sorted(scores, key=itemgetter('score'), reverse=True))

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


def get_scores(year, week, games):
    scores = []
    for game in games:
        try:
            title = '{} vs. {}'.format(game['home_team'], game['away_team'])
            print(title)
            score, play_by_play = compute_score(game)
            print('Final score: {}\n\n'.format(score))
            scores.append({'title': title, 'score': score})
            store_score(year, week, score, game, play_by_play)
        except Exception as e:
            print(e)
    return scores


def store_score(year, week, score, game, play_by_play):
    computed_score_table.put_item(
        Item={
            'year:week': '{}:{}'.format(year, week),
            'score': Decimal(str(score)),
            'away': game['away_team'],
            'home': game['home_team'],
            'play-by-play': list(map(lambda x: Decimal(str(x)), play_by_play)),
        }
    )
