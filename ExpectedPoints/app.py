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
    gen_drive_score(week, 401013357, 0)
    gen_drive_score(week, 401013357, 1)
    gen_drive_score(week, 401013357, 5)


def gen_drive_score(week, game_id, drive_index):
    drive = week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == drive_index)]
    scoring_play_frame = drive.loc[(drive['isScoringPlay'] == True)]
    scoring_play = scoring_play_frame.iloc[0] if not scoring_play_frame.empty else None

    if scoring_play is None:
        print("No score on this drive")
        return 0

    previous_play = get_previous_play(week, scoring_play)
    print(previous_play)


def get_previous_play(week, current):
    print()
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

    return week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == previous_drive_index) & (week['playIndex'] == previous_play_index)]

if __name__ == "__main__":
    main()
