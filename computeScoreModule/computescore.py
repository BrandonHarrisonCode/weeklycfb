import requests
import json
import urllib
from winprobability import play_win_probability, pregame_win_probability, postgame_win_probability, moving_average
from operator import itemgetter


def compute_score(game):
    url = create_plays_url(game)
    print('URL for play data: {}'.format(url))
    home_team = game['home_team']
    vegas_line = get_vegas_line(game)

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


def create_vegas_line_url(game):
    base = 'https://api.collegefootballdata.com/lines?seasonType=both&year={}&week={}&home={}&away={}'
    url = base.format(game['season'], game['week'], game['home_team'], game['away_team'])
    return url


def get_vegas_line(game):
    url = create_vegas_line_url(game)
    print('URL for line data: {}'.format(url))

    result = requests.get(url)
    if not result.ok:
        print('Could not load betting lines')
        return 0
    content = json.loads(result.content)[0]
    lines = content.get('lines')
    if lines is None or len(lines) == 0:
        print('No betting lines stored for play')
        return 0

    vegas_line_avg = 0
    for line in lines:
        if line['provider'] == 'consensus':
            print('Vegas line: {}'.format(line['spread']))
            return line['spread']
        else:
            vegas_line_avg += line['spread']
    vegas_line = vegas_line_avg / len(lines)
    print('Vegas line: {}'.format(vegas_line))
    return vegas_line


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
