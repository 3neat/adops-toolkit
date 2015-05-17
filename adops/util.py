import pandas as pd
from os import path


def combine_reports(files, columns, folder):
    # Return an aggregate DataFrame for a given set of files

    section = pd.DataFrame()

    for rpt in files:
        report_path = str(path.join(folder, rpt.filename))
        df = pd.read_csv(report_path,
                         usecols=columns,
                         sep='\t')
        section = pd.concat([section, df])
    return section


def add_metrics(df):

    df['ctr'] = df.clicks / df.impressions
    df['win_rate'] = df.impressions / df.bids
    df['avg_bid'] = df.bid_amount / df.bids * 1000
    df['tc'] = df.ctc_1 + df.vtc_1 + df.ctc_2 + df.vtc_2 + df.ctc_3 + df.vtc_3 + df.ctc_4 + df.vtc_4 + df.ctc_5 + df.vtc_5
    df['ecpc'] = df.cost / df.clicks
    df['ecpm'] = df.cost / df.impressions * 1000
    df['ecpa'] = df.cost / df.tc
    df['moat'] = df.creative_was_viewable / df.creative_is_trackable
    return df