import os
import datetime
import pandas as pd


def check_import_status():
    print('import ok')


def create_savedir(root_dir, site_tofill, srs_chamber):

    timestamp = datetime.datetime.now().strftime("_%y%m%d")
    savedir = root_dir + '\\' + site_tofill + '_' + srs_chamber + '_' + timestamp
    print(savedir)
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    return savedir


def read_csv(csvpath):
    df = pd.read_csv(csvpath)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.set_index('timestamp', inplace=True)
    elif 'date' in df.columns:
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


def dataset_split(dataset, SRS_CHAMBER):
    # find missing data index
    missingdata_index = dataset[dataset[SRS_CHAMBER].isnull()].index
    print(missingdata_index)
    # drop the missing index so the rest of the data are available for training
    available_data = dataset.drop(missingdata_index, axis=0)
    print(available_data.shape)

    # split
    train = available_data.sample(frac=0.8, random_state=200)
    test = available_data.drop(train.index)
    print(train.shape, test.shape)

    y_train = train.filter([SRS_CHAMBER]).copy()
    print(y_train.shape)  # training input features

    x_train = train.drop([SRS_CHAMBER], axis=1)
    print(x_train.shape)  # training target

    y_test = test.filter([SRS_CHAMBER]).copy()
    print(y_test.shape)  # testing input features

    x_test = test.drop([SRS_CHAMBER], axis=1)
    print(x_test.shape)  # testing target

    x_predict = dataset[dataset.index.isin(missingdata_index)].drop([
        SRS_CHAMBER], axis=1)
    print(x_predict.shape)

    return x_train, y_train, x_test, y_test, x_predict


def count_by_seasons(df):
    total = len(df)
    df.index = pd.to_datetime(df.index, format='mixed')
    df['month'] = df.index.month
    spring = df.query('month == 3').shape[0] + df.query(
        'month == 4').shape[0] + df.query('month == 5').shape[0]
    summer = df.query('month == 6').shape[0] + df.query(
        'month == 7').shape[0] + df.query('month == 8').shape[0]
    autumn = df.query('month == 9').shape[0] + df.query(
        'month == 10').shape[0] + df.query('month == 11').shape[0]
    winter = df.query('month == 12').shape[0] + df.query(
        'month == 1').shape[0] + df.query('month == 2').shape[0]
    assert total == spring + summer + autumn + winter, 'numbers not match'
    return spring, summer, autumn, winter

# use regex to find SRS CHAMBER LIST


def get_srs_chambers(site_to_fill):
    site_df = read_csv(site_dict[site_to_fill])
    r = re.compile("^FD.*_Flux_Median$", re.IGNORECASE)  # case insensitive
    srs_chambers_list = list(filter(r.match, list(site_df.columns)))
    print(srs_chambers_list)
    return site_df, srs_chambers_list


