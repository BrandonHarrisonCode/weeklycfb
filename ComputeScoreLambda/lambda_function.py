import requests
import json
import scipy.signal
from winprobability import play_win_probability, pregame_win_probability, postgame_win_probability, moving_average
from operator import itemgetter

def lambda_handler(event, context):
    plays_url = 'https://api.collegefootballdata.com/plays?seasonType=regular&year=2018&week=13&team=LSU'
    result = requests.get(plays_url)
    if not result.ok:
        return abort(500)

    home_team = 'Texas A&M'
    vegas_line = -3.0

    plays = json.loads(result.content)
    # plays = filter(lambda i: len(i['clock']) != 0, plays)
    plays = sorted(plays, key=itemgetter('id'))
    win_probabilites = []
    count = 0
    for play in plays:
        print(play)
        win_probability = 1 - play_win_probability(home_team, vegas_line, play)
        print(win_probability)
        if win_probability is not None:
            win_probabilites.append(win_probability)
            count += 1
    smoothed = moving_average(win_probabilites, 3)
    smoothed.insert(0, 1 - pregame_win_probability(home_team, vegas_line))
    smoothed.append(1 - postgame_win_probability(home_team, plays[-1]))
    print([[x, win_probabilites[x]] for x in range(0, len(win_probabilites))])
    print([[x, smoothed[x]] for x in range(0, len(smoothed))])

    return {
        'statusCode': 200
    }


def abort(statuscode):
    return {
        'statusCode': statuscode
    }


if __name__ == '__main__':
    lambda_handler(None, None)
