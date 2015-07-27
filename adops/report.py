from os import path
from hashlib import sha1
from datetime import datetime
import re
import pandas as pd
import numpy as np


class Report(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = path.basename(self.filepath)

        tmp = parse_filename(self.filename)
        self.report_type = tmp['report_type']
        self.start_date = tmp['report_start_date']
        self.end_date = tmp['report_end_date']
        self.report_length = tmp['report_length']
        self.advertiser = tmp['advertiser']
        self.advertiser_id = tmp['advertiser_id']

        self.og_columns = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Advertiser Name', 'Campaign Name',
                           'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4',
                           'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost',
                           'CreativeIsTrackable', 'CreativeWasViewable']
        self.rn_columns = ['advertiser_id', 'campaign_id', 'adgroup_id', 'advertiser_name', 'campaign_name',
                           'adgroup_name', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3',
                           'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost',
                           'creative_is_trackable', 'creative_was_viewable']

    def githash(self):
        self.s = sha1()
        self.data = open(self.filepath, 'r')
        self.s.update("blob %u\0" % len(self.data.read()))
        return self.s.hexdigest()

    def to_df(self, rename_cols=False):
        self.df = pd.read_csv(self.filepath,
                         usecols=self.og_columns,
                         sep='\t')
        if rename_cols:
            self.df.columns = self.rn_columns
        return self.df

    def __str__(self):
        return "%s for %s" % (self.report_type, self.advertiser)

class SiteReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Ad Format', 'Site', 'Supply Vendor',
                           'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks',
                           'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5',
                           'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
        self.rn_columns = ['advertiser_id', 'campaign_id', 'adgroup_id', 'ad_format', 'site', 'supply_vendor',
                           'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions',
                           'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3',
                           'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']

class SiteListReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Matched Site Strategy Line Id',
                           'Matched Fold Strategy Line Id', 'Advertiser Name', 'Campaign Name', 'Ad Group Name',
                           'Site Placement Adjustment Line Name', 'Site', 'Category', 'Site Adjustment', 'Fold',
                           'Fold Adjustment', 'Bids', 'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4',
                           'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost',
                           'Category Id', 'Category Hierarchy', 'Matched Site List Id', 'Matched Site List Name',
                           'CreativeIsTrackable', 'CreativeWasViewable']
        self.rn_columns = ['advertiser_id', 'campaign_id', 'adgroup_id', 'matched_site_strategy_line_id',
                           'matched_fold_strategy_line_id', 'advertiser_name', 'campaign_name', 'adgroup_name',
                           'site_placement_adjustment_line_name', 'site', 'category', 'site_adjustment', 'fold',
                           'fold_adjustment', 'bids', 'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3',
                           'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost',
                           'category_id', 'category_hierarchy', 'matched_site_list_id', 'matched_site_list_name',
                           'creative_is_trackable', 'creative_was_viewable']

class DataElementReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Date', 'Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Data Element Id', 'Advertiser Name',
                           'Campaign Name', 'Ad Group Name', 'Data Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks',
                           'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5',
                           'PI 6', 'Advertiser Total Cost', 'Third Party Data Brand Name', 'CreativeIsTrackable',
                           'CreativeWasViewable']
        self.rn_columns = ['date', 'advertiser_id', 'campaign_id', 'adgroup_id', 'data_element_id', 'advertiser_name',
                           'campaign_name', 'adgroup_name', 'data_name', 'bids', 'bid_amount', 'impressions', 'clicks',
                           'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4',
                           'vtc_5', 'vtc_6', 'cost', 'third_party_data_brand', 'creative_is_trackable',
                           'creative_was_viewable']

class TimeOfDayReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Date', 'UTC Hour', 'User Hour of Week', 'Advertiser Id', 'Campaign Id', 'Ad Group Id',
                           'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps', 'Clicks',
                           'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4', 'PI 5',
                           'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
        self.rn_columns = ['date', 'utc_hour', 'user_hour_of_week', 'advertiser_id', 'campaign_id', 'adgroup_id',
                           'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions',
                           'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3',
                           'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']

class BrowserReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Device Type', 'OS Family', 'OS', 'Browser',
                           'Ad Format', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount',
                           'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3',
                           'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable',
                           'CreativeWasViewable']
        self.rn_columns = ['advertiser_id', 'campaign_id', 'adgroup_id', 'device_type', 'os_family', 'os', 'browser',
                           'ad_format', 'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount',
                           'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1',
                           'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable',
                           'creative_was_viewable']

class AdGroupRecencyReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Audience Id',
                           'Recency Bucket Start In Minutes', 'RecencyBucketEndInMinutes', 'Advertiser Name',
                           'Campaign Name', 'Ad Group Name', 'Audience Name', 'Recency Bucket Name', 'Bids',
                           'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1',
                           'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable',
                           'CreativeWasViewable']
        self.rn_columns = ['advertiser_id', 'campaign_id', 'adgroup_id', 'audience_id',
                           'recency_bucket_start_in_minutes', 'recency_bucket_end_in_minutes', 'advertiser_name',
                           'campaign_name', 'adgroup_name', 'audience_name', 'recency_bucket_name', 'bids',
                           'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6',
                           'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable',
                           'creative_was_viewable']

class PerformanceReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Date', 'Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Ad Format', 'Creative Id',
                           'Frequency', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Creative Name', 'Bids',
                           'Bid Amount', 'Imps', 'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1',
                           'PI 2', 'PI 3', 'PI 4', 'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable',
                           'CreativeWasViewable']
        self.rn_columns = ['date', 'advertiser_id', 'campaign_id', 'adgroup_id', 'ad_format', 'creative_id',
                           'frequency', 'advertiser_name', 'campaign_name', 'adgroup_name', 'creative_name', 'bids',
                           'bid_amount', 'impressions', 'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6',
                           'vtc_1', 'vtc_2', 'vtc_3', 'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable',
                           'creative_was_viewable']

class GeoReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Advertiser Id', 'Campaign Id', 'Ad Group Id', 'Country', 'Region', 'Metropolitan Area',
                           'City', 'Advertiser Name', 'Campaign Name', 'Ad Group Name', 'Bids', 'Bid Amount', 'Imps',
                           'Clicks', 'PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PI 1', 'PI 2', 'PI 3', 'PI 4',
                           'PI 5', 'PI 6', 'Advertiser Total Cost', 'CreativeIsTrackable', 'CreativeWasViewable']
        self.rn_columns = ['advertiser_id', 'campaign_id', 'adgroup_id', 'country', 'region', 'metro_area', 'city',
                           'advertiser_name', 'campaign_name', 'adgroup_name', 'bids', 'bid_amount', 'impressions',
                           'clicks', 'ctc_1', 'ctc_2', 'ctc_3', 'ctc_4', 'ctc_5', 'ctc_6', 'vtc_1', 'vtc_2', 'vtc_3',
                           'vtc_4', 'vtc_5', 'vtc_6', 'cost', 'creative_is_trackable', 'creative_was_viewable']

def parse_filename(filename):
    # Parse the filename for all metadata
    regex = re.compile(r'.*Advertiser - (?P<advertiser>.*) - (?P<advertiser_id>\w{7}) - (RTB )?(?P<report_type>.*)'
                       r' - (?P<report_length>\d{1,2} Days) - USD - (?P<report_start_date>\d{8})-'
                       r'(?P<report_end_date>\d{8})\.tsv$')

    match = regex.match(filename)
    if match:
        file_info = match.groupdict()
        file_info['filename'] = filename
        file_info['report_start_date'] = datetime.strptime(file_info['report_start_date'], '%Y%m%d')
        file_info['report_end_date'] = datetime.strptime(file_info['report_end_date'], '%Y%m%d')
        return file_info
    else:
        print "Unexpected file type or name: " + filename


def report_filter(reports, **view):
    # TODO: 1 - Implement unit testing for this function

    # Filter reports by: Type
    reports = [r for r in reports if r.report_type == view['report_type']]

    # Filter reports by: Advertiser
    if view['advertiser'] is not None:
        reports = [r for r in reports if r.advertiser_id in view['advertiser']]

    # Filter reports by: Date Range
    filtered_list = []
    if view['date_range'] is not None:
        for r in reports:
            now = datetime.now()
            delta = now - r.end_date

            if int(delta.days) <= view['date_range']:
                # TODO: 3 - This should eventually become the basis of logging
                #print r.filename + " " + str(delta.days)
                filtered_list.append(r)

        reports = filtered_list
    return reports