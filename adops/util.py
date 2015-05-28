import pandas as pd
import numpy as np
from os import path
from adops import report


# STATIC columns, new names
SITE_COLUMNS = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Site', 'Supply Vendor', 'Advertiser Name',
                          'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2',
                          'PC 3', 'PC 4', 'PC 5', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'Advertiser Total Cost',
                          'CreativeIsTrackable', 'CreativeWasViewable']

SITE_NAME = ['advertiser_id', 'campaign_id', 'adgroup_id', 'site', 'supply_vendor', 'advertiser_name',
                        'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks',
                        'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'vtc_1','vtc_2', 'vtc_3', 'vtc_4', 'vtc_5',
                        'cost', 'creative_is_trackable', 'creative_was_viewable']

SITE_NEW_NAME = ['advertiser_id', 'campaign_id', 'adgroup_id', 'site', 'supply_vendor', 'advertiser_name',
                        'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks',
                        'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'vtc_1','vtc_2', 'vtc_3', 'vtc_4', 'vtc_5',
                        'cost', 'creative_is_trackable', 'creative_was_viewable','ctr', 'win_rate', 'avg_bid', 'tc',
                        'ecpc', 'ecpm', 'ecpa', 'moat']

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
    # Add common metrics to DataFrame
    df['ctr'] = df.clicks / df.impressions
    df['win_rate'] = df.impressions / df.bids
    df['avg_bid'] = df.bid_amount / df.bids * 1000
    df['tc'] = df.ctc_1 + df.vtc_1 + df.ctc_2 + df.vtc_2 + df.ctc_3 + df.vtc_3 + df.ctc_4 + df.vtc_4 + df.ctc_5 + df.vtc_5
    df['ecpc'] = df.cost / df.clicks
    df['ecpm'] = df.cost / df.impressions * 1000
    df['ecpa'] = df.cost / df.tc
    df['moat'] = df.creative_was_viewable / df.creative_is_trackable
    return df


def create_report(folder, reports, view):
    # Filter out the needed report files for analysis
    filtered_reports = report.report_filter(reports, **view)

    # Transform report files to working DataFrame
    df = combine_reports(filtered_reports, SITE_COLUMNS, folder)
    df.columns = SITE_NAME

    df = df.groupby('site')
    df = df[[x for x in SITE_NAME]].aggregate(np.sum)

    df = add_metrics(df)

    df.to_csv(''.join([view['name'], '.csv']))