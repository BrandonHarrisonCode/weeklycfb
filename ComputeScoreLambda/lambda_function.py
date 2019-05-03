import requests
import json
from computescore import compute_score
from operator import itemgetter

def lambda_handler(event, context):
    url = 'https://api.collegefootballdata.com/games?year=2018&week=13&seasonType=both'
    games = get_games(url)

    # games = filter(lambda x: x['away_team'] == 'LSU', games)
    scores = []
    for game in games:
        try:
            title = '{} vs. {}'.format(game['home_team'], game['away_team'])
            print(title)
            score = compute_score(game)
            print('Final score: {}\n\n'.format(score))
            scores.append({'title': title, 'score': score})
        except Exception as e:
            print(e)
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
        raise IOError('Could not access API')
    data = json.loads(result.content)
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


if __name__ == '__main__':
    lambda_handler(None, None)
