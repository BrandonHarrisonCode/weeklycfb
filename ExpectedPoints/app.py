import argparse

import numpy as np
import pandas as pd

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(usage=__doc__)
    # parser.add_argument("--order", type=int, default=8, help="order of Bessel function")
    # parser.add_argument("--output", default="plot.png", help="output image file")
    args = parser.parse_args()

    week = pd.read_csv('PBP2018Week1.csv', quotechar='"',)
    # avg = week.groupby(['down', 'distance'])['yardLine'].mean()
    print('drive_score = {}'.format(gen_drive_score(week, 401013357, 0))) # Nothing happens
    print('drive_score = {}'.format(gen_drive_score(week, 401013357, 1))) # Touchdown on one play home
    print('drive_score = {}'.format(gen_drive_score(week, 401013357, 5))) # Extended drive to touchdown home
    print('drive_score = {}'.format(gen_drive_score(week, 401013357, 8))) # Field goal for away
    print('drive_score = {}'.format(gen_drive_score(week, 401014972, 21))) # Safety


def gen_drive_score(week, game_id, drive_index):
    drive = week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == drive_index)]
    scoring_play = get_scoring_play(drive)

    if scoring_play is None:
        return 0

    previous_play = get_previous_play(week, scoring_play)
    home_has_possession = scoring_play.get('homeId') == scoring_play.get('offenseId')
    home_score_difference = scoring_play.get('homeScore') - previous_play.get('homeScore')
    away_score_difference = scoring_play.get('awayScore') - previous_play.get('awayScore')
    if home_has_possession:
        return home_score_difference - away_score_difference
    else:
        return away_score_difference - home_score_difference


def get_scoring_play(drive):
    scoring_play_frame = drive.loc[(drive['isScoringPlay'] == True)]
    scoring_play = scoring_play_frame.iloc[0] if not scoring_play_frame.empty else None
    return scoring_play


def get_previous_play(week, current):
    game_id = current.get('gameId')
    drive_index = current.get('driveIndex')
    play_index = current.get('playIndex')

    previous_play_index = play_index - 1
    previous_drive_index = drive_index
    if previous_play_index < 0:
        previous_drive_index -= 1
        if previous_drive_index < 0:
            return None
        previous_drive = week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == previous_drive_index)]
        previous_play_index = previous_drive['playIndex'].max()

    return week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == previous_drive_index) & (week['playIndex'] == previous_play_index)].iloc[0]

if __name__ == "__main__":
    main()
