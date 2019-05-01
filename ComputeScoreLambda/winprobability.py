from expectedpoints import get_expected_points
from math import sqrt
from scipy.stats import norm

# Values taken from https://www.pro-football-reference.com/about/win_prob.htm
start_std_dev_scoring_margin = 13.45
rounding_limit = .5
win_probability_if_tie = .5

# home_vegas_line is the amount that the home team is expected to win by * -1
# expected points is negative if the home team has possession or positive otherwise
# Away margin is negative if home team is leading and positive if otherwise
def play_win_probability():
    game_left = 10 / 60
    inverse_game_left = game_left ** -1
    home_vegas_line = -3
    expected_points = 4.24
    away_margin = -7 + expected_points

    scaled_std_dev_scoring_margin = start_std_dev_scoring_margin / sqrt(inverse_game_left)
    scaled_vegas_line = -home_vegas_line * game_left
    prob_lose_regulation = norm.cdf(away_margin + rounding_limit, scaled_vegas_line, scaled_std_dev_scoring_margin)
    prob_win_regulation = norm.cdf(away_margin - rounding_limit, scaled_vegas_line, scaled_std_dev_scoring_margin)
    prob_of_tie = abs(prob_lose_regulation - prob_win_regulation)
    prob_win = 1 - prob_lose_regulation + win_probability_if_tie * prob_of_tie

    return prob_win
