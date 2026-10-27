"""Build a trial-level data file (one row per trial) from raw MB5 PsychoPy/Tobii csv files.

Usage:  python generate_mb5_trials_data.py
You will be prompted for the data directory, lab_id, familiarization_type and output path.
"""
import glob
import os

import numpy as np
import pandas as pd

TRIAL_DATA_COLUMNS = ['lab_id', 'participant_id', 'familiarization_type', 'trial_num', 'familiarization_condition',
    'familiar_stimulus_filename', 'novel_stimulus_filename', 'familiarization_stimulus_screen_time',
    'familiarization_stimulus_looking_time', 'test_1_novel_stimulus_side', 'test_1_looking_time_novel',
    'test_1_looking_time_familiar', 'test_1_trial_time', 'test_2_novel_stimulus_side', 'test_2_looking_time_novel',
    'test_2_looking_time_familiar', 'test_2_trial_time', 'trial_error', 'trial_error_info', 'notes']

DURATION_COLUMNS = ['familiarization_stimulus_screen_time', 'familiarization_stimulus_looking_time',
    'test_1_looking_time_novel', 'test_1_looking_time_familiar', 'test_1_trial_time',
    'test_2_looking_time_novel', 'test_2_looking_time_familiar', 'test_2_trial_time']

FAMILIARIZATION_TYPES = ['infant-controlled', 'fixed-length']


def _last(series):
    s = series.dropna()
    return s.iloc[-1] if len(s) else np.nan


def _first(series):
    s = series.dropna()
    return s.iloc[0] if len(s) else np.nan


def _with_png(name):
    if pd.isna(name):
        return name
    name = str(name)
    return name if name.lower().endswith('.png') else name + '.png'


def _novel_side(familiar_location):
    if familiar_location == 'left':
        return 'right'
    if familiar_location == 'right':
        return 'left'
    return np.nan


def file_to_trial_data(df):
    """Convert one raw PsychoPy/Tobii data frame to one row per trial."""
    df = df.reset_index(drop=True)
    df = df[df['trial_number'].notna()].copy()
    df['test_period_num'] = df['Test_Period.started'].notna().groupby(df['trial_number']).cumsum()
    for col in ['gaze_time_in_roi_left', 'gaze_time_in_roi_right']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    rows = []
    for trial_number, t in df.groupby('trial_number', sort=True):
        row = dict.fromkeys(TRIAL_DATA_COLUMNS, np.nan)
        row.update(
            participant_id=_first(t['participant']),
            trial_num=trial_number,
            familiarization_condition=_first(t['familiarization_time']),
            familiar_stimulus_filename=_with_png(_first(t['familiar_stimulus'])),
            novel_stimulus_filename=_with_png(_first(t['novel_stimulus'])),
            familiarization_stimulus_screen_time=_first(t['Familiarization.stopped']) - _first(t['Familiarization.started']),
            familiarization_stimulus_looking_time=_last(t['gaze_time_ROI_familiarization']),
            trial_error='no_error',
            trial_error_info='NA',
            notes=_first(t['notes']) if pd.notna(_first(t['notes'])) else 'NA',
        )
        for n in (1, 2):
            fam_loc = _first(t[f'familiar_location_{n}'])
            p = t[t['test_period_num'] == n]
            left, right = _last(p['gaze_time_in_roi_left']), _last(p['gaze_time_in_roi_right'])
            fam_left = fam_loc == 'left'
            row[f'test_{n}_novel_stimulus_side'] = _novel_side(fam_loc)
            row[f'test_{n}_looking_time_novel'] = right if fam_left else left
            row[f'test_{n}_looking_time_familiar'] = left if fam_left else right
            # stop timestamps are logged on a later row than the start, so pair the n-th start with the n-th stop
            starts, stops = t['Test_Period.started'].dropna(), t['Test_Period.stopped'].dropna()
            row[f'test_{n}_trial_time'] = stops.iloc[n - 1] - starts.iloc[n - 1] if min(len(starts), len(stops)) >= n else np.nan
        rows.append(row)
    out = pd.DataFrame(rows, columns=TRIAL_DATA_COLUMNS)
    # raw timings are in seconds; report all measured durations in ms
    out[DURATION_COLUMNS] = out[DURATION_COLUMNS].astype(float) * 1000
    # whole-number columns (nullable Int64 avoids 5.0 / 1.0 in the csv)
    out[['familiarization_condition', 'trial_num']] = out[['familiarization_condition', 'trial_num']].astype('Int64')
    return out


def build_trial_data(data_dir='data', pattern='*.csv', lab_id=np.nan, familiarization_type=np.nan):
    """Run file_to_trial_data over every matching csv in data_dir and stack the results."""
    frames = [file_to_trial_data(pd.read_csv(path, low_memory=False))
              for path in sorted(glob.glob(os.path.join(data_dir, pattern)))]
    if not frames:
        return pd.DataFrame(columns=TRIAL_DATA_COLUMNS)
    out = pd.concat(frames, ignore_index=True)
    # manual-entry columns
    out['lab_id'] = lab_id
    out['familiarization_type'] = familiarization_type
    return out


def prompt_required(label):
    """Ask until a non-empty answer is given."""
    while True:
        answer = input(f'Enter {label}: ').strip()
        if answer:
            return answer
        print(f'{label} cannot be empty.')


def prompt_choice(label, options):
    """Ask until one of the options is chosen, by number or by name."""
    menu = ', '.join(f'{i}) {o}' for i, o in enumerate(options, 1))
    while True:
        answer = input(f'Enter {label} - {menu}: ').strip().strip('"\'').lower()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        if answer in options:
            return answer
        print(f'Please choose one of: {menu}')


def prompt_directory(label='path to the data directory'):
    """Ask until an existing directory containing at least one csv file is given."""
    while True:
        path = os.path.expanduser(input(f'Enter {label}: ').strip().strip('"\''))
        if not os.path.isdir(path):
            print(f'{path!r} is not a directory.')
        elif not glob.glob(os.path.join(path, '*.csv')):
            print(f'No .csv files found in {path!r}.')
        else:
            return path


def prompt_output_path(default_name='trial_data.csv'):
    """Ask for an output csv path (or a directory, which gets default_name); confirm before overwriting."""
    while True:
        path = os.path.expanduser(input(f'Enter output path (.csv file or directory) [{default_name}]: ').strip().strip('"\'') or '.')
        if os.path.isdir(path) or path in ('.', '') or not os.path.splitext(path)[1]:
            path = os.path.join(path, default_name)
        elif not path.lower().endswith('.csv'):
            print('Output file must end in .csv.')
            continue
        if os.path.exists(path) and input(f'{path} exists. Overwrite? [y/N]: ').strip().lower() != 'y':
            continue
        return path


def save_trial_data(df, path):
    """Write df to path as csv, creating parent folders if needed."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    df.to_csv(path, index=False)
    print(f'Saved {len(df)} rows to {path}')


def main():
    data_dir = prompt_directory()
    lab_id = prompt_required('lab_id')
    familiarization_type = prompt_choice('familiarization_type', FAMILIARIZATION_TYPES)
    output_path = prompt_output_path()

    trial_data = build_trial_data(data_dir, lab_id=lab_id, familiarization_type=familiarization_type)
    save_trial_data(trial_data, output_path)


if __name__ == '__main__':
    main()
