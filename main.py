import os
import numpy as np
from adops import report, util

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


def init_reports(folder):
    # TODO: 3 - May want to consider refactoring this to pass entire path; verify for cross OS compatibility
    rpt = []
    for f in os.listdir(folder):
        if f.endswith(".tsv"):
            rpt.append(report.Report(f))
    return rpt





# Set testing variables
current_directory = os.getcwd()
folder = os.path.join(current_directory, 'reports/')
reports = init_reports(folder)
report_type = 'Site'
advertiser = ['xbci0tw', 'nk6bz6j']


date_range = 80

# Filter out the needed report files for analysis
filtered_reports = report.report_filter(reports,report_type,advertiser,date_range)

# Transform report files to working DataFrame
df = util.combine_reports(filtered_reports, SITE_COLUMNS, folder)
df.columns = SITE_NAME

df = df.groupby('site')
df = df[[x for x in SITE_NAME]].aggregate(np.sum)

df = util.add_metrics(df)

# NOTES:
# * All of the above functions will produce an advertiser / filtered Site Report data frame
# that has performance metrics calculated and is ready for analysis. It still needs the ability to:
# TODO: 0 - Create these data frames based on saved "rule/group" structure
# TODO: 0 - After a rule structure, need to think of UI
# TODO: 1 - Refactor below to __main__
for x in filtered_reports:
    print x.filepath