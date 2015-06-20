import pandas as pd
import numpy as np
from os import path
from adops import report


def get_columns(report_type):
    ###########################################
    # Column Headers
    ###########################################
    SITE_COLUMNS = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Ad Format', 'Site', 'Supply Vendor', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
    SITELIST_COLUMNS =	['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Matched Site Strategy Line Id', 'Matched Fold Strategy Line Id', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Site Placement Adjustment Line Name', 'Site', 'Category', 'Site Adjustment', 'Fold', 'Fold Adjustment', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'Category Id', 'Category Hierarchy', 'Matched Site List Id', 'Matched Site List Name', 'CreativeIsTrackable', 'CreativeWasViewable']
    DATAELEMENTS_COLUMNS = ['Date', 'Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Data Element Id', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Data Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'Third Party Data Brand Name', 'CreativeIsTrackable', 'CreativeWasViewable']
    TIMEOFDAY_COLUMNS = ['Date', 'UTC Hour', 'User Hour of Week', 'Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
    BROWSER_COLUMNS = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Device Type', 'OS Family', 'OS', 'Browser', 'Ad Format', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
    RECENCY_COLUMNS = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Audience Id', 'Recency Bucket Start In Minutes', 'RecencyBucketEndInMinutes', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Audience Name', 'Recency Bucket Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
    PERFORMANCE_COLUMNS = ['Date', 'Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Ad Format', 'Creative Id', 'Frequency', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Creative Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
    GEOGRAPHY_COLUMNS = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Country', 'Region', 'Metropolitan Area', 'City', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
    ###########################################
    # New Names
    ###########################################
    SITE_NAMES = ['advertiser_id', 'campaign_id', 'adgroup_id', 'ad_format', 'site', 'supply_vendor', 'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']
    SITELIST_NAMES = ['advertiser_id', 'campaign_id', 'adgroup_id', 'matched_site_strategy_line_id', 'matched_fold_strategy_line_id', 'advertiser_name', 'campaign_name', 'adgroup_name', 'site_placement_adjustment_line_name', 'site', 'category', 'site_adjustment', 'fold', 'fold_adjustment', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'category_id', 'category_hierarchy', 'matched_site_list_id', 'matched_site_list_name', 'creative_is_trackable', 'creative_was_viewable']
    DATAELEMENTS_NAMES = ['date', 'advertiser_id', 'campaign_id', 'adgroup_id', 'data_element_id', 'advertiser_name', 'campaign_name', 'adgroup_name', 'data_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'third_party_data_brand', 'creative_is_trackable', 'creative_was_viewable']
    TIMEOFDAY_NAMES = ['date', 'utc_hour', 'user_hour_of_week', 'advertiser_id', 'campaign_id', 'adgroup_id', 'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']
    BROWSER_NAMES = ['advertiser_id', 'campaign_id', 'adgroup_id', 'device_type', 'os_family', 'os', 'browser', 'ad_format', 'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']
    RECENCY_NAMES = ['advertiser_id', 'campaign_id', 'adgroup_id', 'audience_id', 'recency_bucket_start_in_minutes', 'recency_bucket_end_in_minutes', 'advertiser_name', 'campaign_name', 'adgroup_name', 'audience_name', 'recency_bucket_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']
    PERFORMANCE_NAMES = ['date', 'advertiser_id', 'campaign_id', 'adgroup_id', 'ad_format', 'creative_id', 'frequency', 'advertiser_name', 'campaign_name', 'adgroup_name', 'creative_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']
    GEOGRAPHY_NAMES = ['advertiser_id', 'campaign_id', 'adgroup_id', 'country', 'region', 'metro_area', 'city', 'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']

    if report_type == 'Site':
        columns = SITE_COLUMNS
        renamed_columns = SITE_NAMES
    elif report_type == 'Site List':
        columns = SITELIST_COLUMNS
        renamed_columns = SITELIST_NAMES
    elif report_type == 'Data Element Report':
        columns = DATAELEMENTS_COLUMNS
        renamed_columns = DATAELEMENTS_NAMES
    elif report_type == 'Time of Day':
        columns = TIMEOFDAY_COLUMNS
        renamed_columns = TIMEOFDAY_NAMES
    elif report_type == 'Browser Report':
        columns = BROWSER_COLUMNS
        renamed_columns = BROWSER_NAMES
    elif report_type == 'Ad Group Recency':
        columns = RECENCY_COLUMNS
        renamed_columns = RECENCY_NAMES
    elif report_type == 'Performance':
        columns = PERFORMANCE_COLUMNS
        renamed_columns = PERFORMANCE_NAMES
    elif report_type == 'Geo Report':
        columns = GEOGRAPHY_COLUMNS
        renamed_columns = GEOGRAPHY_NAMES
    else:
        print ''.join(["Column error w/ following report type: ", report_type])
    return (columns, renamed_columns)


def adgroup_filter(df, adgroups):
    # isinstance() let's us take in either a string or a list
    if isinstance(adgroups, basestring):
        df = df[df['Ad Group Id'].isin([adgroups])]
    else:
        df = df[df['Ad Group Id'].isin(adgroups)]
    return df


def campaign_filter(df, campaign_id):
    # isinstance() let's us take in either a string or a list
    if isinstance(campaign_id, basestring):
        print "found a string"
        df = df[df['Campaign Id'].isin(list(campaign_id))]
    else:
        df = df[df['Campaign Id'].isin(campaign_id)]
    return df


def combine_reports(reports, folder, view, columns):
    # Return an aggregate DataFrame for a given set of files
    section = pd.DataFrame()

    for rpt in reports:
        df = pd.read_csv(rpt.filepath,
                         usecols=columns,
                         sep='\t')

        if view["campaign"]:
            df = campaign_filter(df, view["campaign"])

        if view["adgroup"]:
            df = adgroup_filter(df, view["adgroup"])

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


def rules_filter(df, rules):
    t = pd.DataFrame()
    for rule in rules:
        t = pd.concat([t, df.query(rule)])
    t.drop_duplicates(inplace=True)
    return t


def create_report(folder, reports, view, group_by):
    # Filter out the needed report files for analysis
    filtered_reports = report.report_filter(reports, **view)
    report_columns, report_name = get_columns(view['report_type'])

    # Transform report files to working DataFrame
    # TODO: 1.a - Refactor this out so that it uses report.filepath instead
    df = combine_reports(filtered_reports, folder, view, report_columns)
    df.columns = report_name

    df = df.groupby(group_by)
    df = df[[x for x in report_name]].aggregate(np.sum)

    df = add_metrics(df)

    if view['rules']:
        df = rules_filter(df, view['rules'])

    df.to_csv(''.join([view['name'], '.csv']))


