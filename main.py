import os
from adops import report, util


def init_reports(folder):
    # TODO: 3 - May want to consider refactoring this to pass entire path; verify for cross OS compatibility
    rpt = []
    for f in os.listdir(folder):
        if f.endswith(".tsv"):
            rpt.append(report.Report(f))
    return rpt

current_directory = os.getcwd()
folder = os.path.join(current_directory, 'reports/')
reports = init_reports(folder)

# Set testing variables
view = {
	'report_type': 'Site',
	'advertiser': ['xbci0tw', 'nk6bz6j'],
	'campaign': [],
	'adgroup': [],
    'date_range': None,
    'name': 'ChannelLock-FranNet_SiteAnalysis'
}

util.create_report(folder, reports, view)

# NOTES:
# * All of the above functions will produce an advertiser / filtered Site Report data frame
# that has performance metrics calculated and is ready for analysis. It still needs the ability to:
# TODO: 0 - Create these data frames based on saved "rule/group" structure
# TODO: 0 - After a rule structure, need to think of UI
# TODO: 1 - Refactor below to __main__
