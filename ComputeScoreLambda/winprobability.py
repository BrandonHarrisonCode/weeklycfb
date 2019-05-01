from expectedpoints import get_expected_points
from math import sqrt
from scipy.stats import norm

# Values taken from https://www.pro-football-reference.com/about/win_prob.htm
start_std_dev_scoring_margin = 13.45
rounding_limit = .5
win_probability_if_tie = .5
minutes_in_quarter = 15
number_of_quarters = 4
seconds_in_minute = 60
yards_in_field = 100

# vegas_line is the amount that the home team is expected to win by * -1
# expected points is negative if the home team has possession or positive otherwise
# Away margin is negative if home team is leading and positive if otherwise
def play_win_probability(home_team, vegas_line, play):
    try:
        game_left = extract_game_left(play)
    except KeyError as e:
        print('Not a play')
        return None
    inverse_game_left = game_left ** -1
    down, yards_to_goal, distance = extract_play_position(home_team, play)
    expected_points = -float(get_expected_points(down, yards_to_goal, distance))
    print('EP: {}'.format(expected_points))
    away_margin = extract_away_margin(home_team, play)
    predicted_away_margin = away_margin + expected_points

    scaled_std_dev_scoring_margin = start_std_dev_scoring_margin / sqrt(inverse_game_left)
    scaled_vegas_line = -vegas_line * game_left
    prob_lose_regulation = norm.cdf(predicted_away_margin + rounding_limit, scaled_vegas_line, scaled_std_dev_scoring_margin)
    prob_win_regulation = norm.cdf(predicted_away_margin - rounding_limit, scaled_vegas_line, scaled_std_dev_scoring_margin)
    prob_of_tie = abs(prob_lose_regulation - prob_win_regulation)
    prob_win = 1 - prob_lose_regulation + win_probability_if_tie * prob_of_tie

    return prob_win


def extract_game_left(play):
    clock = play['clock']
    if clock is None:
        raise KeyError('Not a real play!')
    minutes = play['clock'].get('minutes', 0)
    seconds = play['clock'].get('seconds', 0)
    quarter = play['period']

    print('time: {}, {}, {}'.format(minutes, seconds, quarter))
    min_left = (number_of_quarters - quarter) * minutes_in_quarter + minutes + seconds / seconds_in_minute
    game_left = min_left / (number_of_quarters * minutes_in_quarter)
    print('game left: {}'.format(game_left))
    return game_left


def extract_away_margin(home_team, play):
    offense = play['offense']
    offense_score = int(play['offense_score'])
    defense_score = int(play['defense_score'])

    score = offense_score - defense_score
    away_margin = -score if offense == home_team else score
    print('away margin: {}'.format(away_margin))
    return away_margin


def extract_play_position(home_team, play):
    offense = play['offense']
    yard_line = int(play['yard_line'])
    down = int(play['down'])
    distance = int(play['distance'])

    if offense == home_team:
        yard_line = yards_in_field - yard_line

    print('postion: {}, {}, {}'.format(down, yard_line, distance))
    return down, yard_line, distance
