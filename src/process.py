import os
import datetime
import pandas as pd


def create_savedir(root_dir, site_tofill, srs_chamber):
    
    timestamp = datetime.datetime.now().strftime("_%y%m%d")
    savedir = root_dir + site_tofill + '_' + srs_chamber + '_' + timestamp
    print(savedir)
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    return savedir


def read_csv(csvpath):
    df = pd.read_csv(csvpath)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='mixed')
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.set_index('date', inplace=True)
    elif 'date_time' in df.columns:
        df['date_time'] = pd.to_datetime(df['date_time'], format='mixed')
        df['date_time'] = df['date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.set_index('date_time', inplace=True)
    elif 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], format='mixed')
        df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.set_index('time', inplace=True)
    else:
        print('cant find date index')
    print(df.columns, '\n' 'rows=', len(df))
    return df
