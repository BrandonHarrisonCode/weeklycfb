import requests
import json
from winprobability import play_win_probability, extract_game_left
from operator import itemgetter

def lambda_handler(event, context):
    game_url = 'https://api.collegefootballdata.com/games?year=2018&week=1&seasonType=regular&team=Texas'
    plays_url = 'https://api.collegefootballdata.com/plays?seasonType=regular&year=2018&week=1&team=Texas'
    result = requests.get(plays_url)
    if not result.ok:
        return abort(500)
    plays = json.loads(result.content)
    plays = filter(lambda i: len(i['clock']) != 0, plays)
    plays = sorted(plays, key=extract_game_left, reverse=True)
    win_probabilites = []
    count = 0
    for play in plays:
        print(play)
        win_probability = 1 - play_win_probability("Maryland", 13.5, play)
        print(win_probability)
        if win_probability is not None:
            win_probabilites.append([count, win_probability])
            count += 1
            print('\n\n')
    print('{}: {}'.format(len(win_probabilites), win_probabilites))

    return {
        'statusCode': 200
    }


def abort(statuscode):
    return {
        'statusCode': statuscode
    }


if __name__ == '__main__':
    print(lambda_handler(None, None))
