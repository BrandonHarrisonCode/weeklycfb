import numpy as np
import pandas as pd
from pathlib import Path

def main():
    csv_files = list(Path("data/").rglob("*.csv"))
    dataframes = []
    for filename in csv_files:
        if str(filename).endswith('all.csv'):
            continue
        new_data = get_expected_points_data(filename)
        if new_data is not None:
            dataframes.append(new_data)
    all_data = pd.concat(dataframes)[['down', 'distance', 'yardsToGo', 'driveScore']]
    # all_data_avg = all_data.groupby(['down', 'distance', 'yardsToGo'])['driveScore'].mean()
    print(all_data)
    independent_vars = all_data[['down', 'distance', 'yardsToGo']]
    dependent_vars = all_data[['driveScore']]
    all_data.to_csv('output/all_data.csv', sep=',')


def get_expected_points_data(filename):
    print('Computing data for {}'.format(filename), flush=True)
    week = None
    try:
        week = pd.read_csv(filename, quotechar='"', error_bad_lines=False)
    except pd.errors.EmptyDataError as e:
        print('ERROR: could not read file')
    if week is None:
        return None

    week['driveScore'] = week.apply(lambda row: gen_drive_score_row(week, row), axis=1)
    week['yardsToGo'] = week.apply(lambda row: gen_yards_to_go(week, row), axis=1)
    week = week.loc[(week['down'] >= 1) & (week['down'] <= 4) & (week['distance'] >= 0) & (week['yardLine'] > 0) & (week['type'] != 'Kickoff') & (week['type'] != 'Timeout') & (week['type'] != 'Penalty')]
    expected_points_raw = week[['down', 'distance', 'yardsToGo', 'driveScore']]
    return expected_points_raw


def gen_yards_to_go(week, row):
    home_has_possession = row.get('homeId') == row.get('offenseId')
    yard_line = row.get('yardLine')
    if home_has_possession:
        return 100 - yard_line
    else:
        return yard_line


def gen_drive_score_row(week, row):
    game_id = row.get('gameId')
    drive_index = row.get('driveIndex')
    return gen_drive_score(week, game_id, drive_index)

def gen_drive_score(week, game_id, drive_index):
    drive = week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == drive_index)]
    last_play = get_last_play(drive)

    if last_play is None:
        return 0

    previous_play = get_previous_play(week, last_play)
    home_has_possession = last_play.get('homeId') == last_play.get('offenseId')

    if previous_play is None:
        home_score_difference = last_play.get('homeScore')
        away_score_difference = last_play.get('awayScore')
    else:
        home_score_difference = last_play.get('homeScore') - previous_play.get('homeScore')
        away_score_difference = last_play.get('awayScore') - previous_play.get('awayScore')
    if home_has_possession:
        return home_score_difference - away_score_difference
    else:
        return away_score_difference - home_score_difference


def get_last_play(drive):
    if drive is None:
        return None
    last_play = drive.loc[drive['playIndex'].idxmax()]
    return last_play


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

    previous_play_dataframe = week.loc[(week['gameId'] == game_id) & (week['driveIndex'] == previous_drive_index) & (week['playIndex'] == previous_play_index)]
    return previous_play_dataframe.iloc[0] if not previous_play_dataframe.empty else None

if __name__ == "__main__":
    main()
