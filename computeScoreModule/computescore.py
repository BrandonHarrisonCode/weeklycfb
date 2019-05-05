import requests
import json
import urllib
from winprobability import play_win_probability, pregame_win_probability, postgame_win_probability, moving_average
from operator import itemgetter

def compute_score(game):
    url = create_plays_url(game)
    print('URL for play data: {}'.format(url))
    home_team = game['home_team']
    vegas_line = 0

    plays = get_plays(url)
    win_probabilites = compute_win_probabilities(plays, home_team, vegas_line)
    smoothed = get_smoothed_data(win_probabilites, vegas_line, game)
    print([[x, smoothed[x]] for x in range(0, len(smoothed))])

    distance = get_distance(smoothed)
    print(distance)
    average_distance = distance / len(smoothed)
    return average_distance, smoothed


def create_plays_url(game):
    params = {'year': game['season'], 'week': game['week'], 'team': game['home_team']}
    base = 'https://api.collegefootballdata.com/plays?seasonType=both&'
    return base + urllib.parse.urlencode(params)


def get_plays(url):
    result = requests.get(url)
    if not result.ok:
        raise IOError('Could not access API')
    plays = json.loads(result.content)
    if len(plays) == 0:
        raise ValueError('No plays found at {}'.format(url))
    return sorted(plays, key=itemgetter('id'))


def compute_win_probabilities(plays, home_team, vegas_line):
    win_probabilites = []
    for play in plays:
        win_probability = 1 - play_win_probability(home_team, vegas_line, play)
        if win_probability is not None:
            win_probabilites.append(win_probability)
    return win_probabilites


def get_smoothed_data(win_probabilites, vegas_line, game):
    smoothed = moving_average(win_probabilites, 3)
    smoothed.insert(0, 1 - pregame_win_probability(vegas_line))
    smoothed.append(1 - postgame_win_probability(game))
    return smoothed


def get_distance(array):
    distance = 0
    for i in range(1, len(array)):
        distance += abs(array[i] - array[i - 1])
    return distance
