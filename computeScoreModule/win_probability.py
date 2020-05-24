import numpy
from expected_points import get_expected_points
from math import sqrt
from scipy.stats import norm

# Values taken from https://www.pro-football-reference.com/about/win_prob.htm
start_std_dev_scoring_margin = 13.45
rounding_limit = .5
win_probability_if_tie = .5
minutes_in_quarter = 15
number_of_quarters = 4
seconds_in_minute = 60
minutes_in_hour = 60
yards_in_field = 100
overtime_equivalent_time = 1 / minutes_in_hour


def win_probability(predicted_away_margin, scaled_vegas_line, scaled_std_dev_scoring_margin):
    prob_lose_regulation = norm.cdf(predicted_away_margin + rounding_limit, scaled_vegas_line, scaled_std_dev_scoring_margin)
    prob_win_regulation = norm.cdf(predicted_away_margin - rounding_limit, scaled_vegas_line, scaled_std_dev_scoring_margin)
    prob_of_tie = abs(prob_lose_regulation - prob_win_regulation)
    prob_win = 1 - prob_lose_regulation + win_probability_if_tie * prob_of_tie

    return prob_win


def pregame_win_probability(vegas_line):
    return win_probability(0, -vegas_line, start_std_dev_scoring_margin)


def postgame_win_probability(game):
    margin = game['home_points'] - game['away_points']
    return 1.0 if margin > 0 else 0.0

# vegas_line is the amount that the home team is expected to win by * -1
# expected points is negative if the home team has possession or positive otherwise
# Away margin is negative if home team is leading and positive if otherwise
def play_win_probability(home_team, vegas_line, play):
    game_left, inverse_game_left = extract_game_left(play)
    down, yards_to_goal, distance = extract_play_position(home_team, play)
    expected_points = -float(get_expected_points(down, yards_to_goal, distance))
    away_margin = extract_away_margin(home_team, play)

    predicted_away_margin = away_margin + expected_points
    scaled_std_dev_scoring_margin = start_std_dev_scoring_margin / sqrt(inverse_game_left)
    scaled_vegas_line = -vegas_line * game_left

    return win_probability(predicted_away_margin, scaled_vegas_line, scaled_std_dev_scoring_margin)


def extract_game_left(play):
    clock = play['clock']
    minutes = play['clock'].get('minutes', 0)
    seconds = play['clock'].get('seconds', 0)
    quarter = play['period']

    if quarter <= 4:
        min_left = (number_of_quarters - quarter) * minutes_in_quarter + minutes + seconds / seconds_in_minute
        game_left = min_left / (number_of_quarters * minutes_in_quarter)
        game_left = max(game_left, ((1 / seconds_in_minute) / minutes_in_hour))
        inverse_game_left = game_left ** -1
        return game_left, inverse_game_left
    else:
        return overtime_equivalent_time, overtime_equivalent_time ** -1


def extract_away_margin(home_team, play):
    offense = play['offense']
    offense_score = int(play['offense_score'])
    defense_score = int(play['defense_score'])

    score = offense_score - defense_score
    away_margin = -score if offense == home_team else score
    return away_margin


def extract_play_position(home_team, play):
    offense = play['offense']
    yard_line = int(play['yard_line'])
    down = int(play['down'])
    distance = int(play['distance'])

    if offense == home_team:
        yard_line = yards_in_field - yard_line

    return down, yard_line, distance


def moving_average(array, points=3):
    cumsum = numpy.cumsum(numpy.insert(array, 0, 0))
    return list((cumsum[points:] - cumsum[:-points]) / float(points))
