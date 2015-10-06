from os import path
from hashlib import sha1
from datetime import datetime
import re
import pandas as pd
from sqlalchemy.dialects import postgresql



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

class ConversionReport(Report):

    def __init__(self, filename):
        Report.__init__(self, filename)

        self.og_columns = ['Conversion Time', 'TDID', 'Conversion Id', 'Order Id', '# Impressions', '# Display Clicks',
                           '# Ad Groups w/ Activity', 'Conversion Type', 'Tracking Tag Name', 'Referrer Url',
                           'Path to Conversion', 'Monetary Value', 'First Impression Time',
                           'First Impression Campaign Id', 'First Impression Campaign Name',
                           'First Impression Ad Group Id', 'First Impression Ad Group Name',
                           'First Impression Creative Id', 'First Impression Creative Name',
                           'First Impression Format', 'Last Impression Time', 'Last Impression Campaign Id',
                           'Last Impression Campaign Name', 'Last Impression Ad Group Id',
                           'Last Impression Ad Group Name', 'Last Impression Creative Id',
                           'Last Impression Creative Name', 'Last Impression Format',
                           'Last Impression Frequency', 'Last Impression FCap', 'Last Impression Site',
                           'Last Impression Categories', 'Last Impression Country', 'Last Impression Region',
                           'Last Impression Metro', 'First Display Click Time', 'First Display Click Campaign Id',
                           'First Display Click Campaign Name', 'First Display Click Ad Group Id',
                           'First Display Click Ad Group Name', 'First Display Click Creative Id',
                           'First Display Click Creative Name', 'First Display Click Format', 'Last Display Click Time',
                           'Last Display Click Campaign Id', 'Last Display Click Campaign Name',
                           'Last Display Click Ad Group Id', 'Last Display Click Ad Group Name',
                           'Last Display Click Creative Id', 'Last Display Click Creative Name',
                           'Last Display Click Format', 'Advertiser Id',
                           'TD 1', 'TD 2', 'TD 3', 'TD 4', 'TD 5', 'TD 6', 'TD 7', 'TD 8', 'TD 9', 'TD 10']

        self.rn_columns = ['conversion_time', 'tdid', 'conversion_id', 'order_id', 'num_of_impressions',
                           'num_of_display_clicks', 'num_of_adgroups_w_activity', 'conversion_type',
                           'tracking_tag_name', 'referrer_url', 'path_to_conversion', 'monetary_value',
                           'first_imp_time', 'first_imp_campaign_id', 'first_imp_campaign_name', 'first_imp_adgroup_id',
                           'first_imp_adgroup_name', 'first_imp_creative_id', 'first_imp_creative_name',
                           'first_imp_format', 'last_imp_time', 'last_imp_campaign_id', 'last_imp_campaign_name',
                           'last_imp_adgroup_id', 'last_imp_adgroup_name', 'last_imp_creative_id',
                           'last_imp_creative_name', 'last_imp_format', 'last_imp_frequency', 'last_imp_fcap',
                           'last_imp_site', 'last_imp_categories', 'last_imp_country', 'last_imp_region',
                           'last_imp_metro', 'first_click_time', 'first_click_campaign_id', 'first_click_campaign_name',
                           'first_click_adgroup_id', 'first_click_adgroup_name', 'first_click_creative_id',
                           'first_click_creative_name', 'first_click_format', 'last_click_time',
                           'last_click_campaign_id', 'last_click_campaign_name', 'last_click_adgroup_id',
                           'last_click_adgroup_name', 'last_click_creative_id', 'last_click_creative_name',
                           'last_click_format', 'advertiser_id',
                           'td_1', 'td_2', 'td_3', 'td_4', 'td_5', 'td_6', 'td_7', 'td_8', 'td_9', 'td_10']

        self.dtype = { 'index': postgresql.BIGINT,
                       'conversion_time': postgresql.TEXT,
                       'tdid': postgresql.TEXT,
                       'conversion_id': postgresql.TEXT,
                       'order_id': postgresql.TEXT,
                       'num_of_impressions': postgresql.BIGINT,
                       'num_of_display_clicks': postgresql.BIGINT,
                       'num_of_adgroups_w_activity': postgresql.BIGINT,
                       'conversion_type': postgresql.TEXT,
                       'tracking_tag_name': postgresql.TEXT,
                       'referrer_url': postgresql.TEXT,
                       'path_to_conversion': postgresql.TEXT,
                       'monetary_value': postgresql.DOUBLE_PRECISION,
                       'first_imp_time': postgresql.TEXT,
                       'first_imp_campaign_id': postgresql.TEXT,
                       'first_imp_campaign_name': postgresql.TEXT,
                       'first_imp_adgroup_id': postgresql.TEXT,
                       'first_imp_adgroup_name': postgresql.TEXT,
                       'first_imp_creative_id': postgresql.TEXT,
                       'first_imp_creative_name': postgresql.TEXT,
                       'first_imp_format': postgresql.TEXT,
                       'last_imp_time': postgresql.TEXT,
                       'last_imp_campaign_id': postgresql.TEXT,
                       'last_imp_campaign_name': postgresql.TEXT,
                       'last_imp_adgroup_id': postgresql.TEXT,
                       'last_imp_adgroup_name': postgresql.TEXT,
                       'last_imp_creative_id': postgresql.TEXT,
                       'last_imp_creative_name': postgresql.TEXT,
                       'last_imp_format': postgresql.TEXT,
                       'last_imp_frequency': postgresql.BIGINT,
                       'last_imp_fcap': postgresql.TEXT,
                       'last_imp_site': postgresql.TEXT,
                       'last_imp_categories': postgresql.TEXT,
                       'last_imp_country': postgresql.TEXT,
                       'last_imp_region': postgresql.TEXT,
                       'last_imp_metro': postgresql.TEXT,
                       'first_click_time': postgresql.TEXT,
                       'first_click_campaign_id': postgresql.TEXT,
                       'first_click_campaign_name': postgresql.TEXT,
                       'first_click_adgroup_id': postgresql.TEXT,
                       'first_click_adgroup_name': postgresql.TEXT,
                       'first_click_creative_id': postgresql.TEXT,
                       'first_click_creative_name': postgresql.TEXT,
                       'first_click_format': postgresql.TEXT,
                       'last_click_time': postgresql.TEXT,
                       'last_click_campaign_id': postgresql.TEXT,
                       'last_click_campaign_name': postgresql.TEXT,
                       'last_click_adgroup_id': postgresql.TEXT,
                       'last_click_adgroup_name': postgresql.TEXT,
                       'last_click_creative_id': postgresql.TEXT,
                       'last_click_creative_name': postgresql.TEXT,
                       'last_click_format': postgresql.TEXT,
                       'advertiser_id': postgresql.TEXT,
                       'td_1': postgresql.BIGINT,
                       'td_2': postgresql.BIGINT,
                       'td_3': postgresql.BIGINT,
                       'td_4': postgresql.BIGINT,
                       'td_5': postgresql.BIGINT,
                       'td_6': postgresql.BIGINT,
                       'td_7': postgresql.BIGINT,
                       'td_8': postgresql.BIGINT,
                       'td_9': postgresql.BIGINT,
                       'td_10': postgresql.BIGINT,
                    }

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