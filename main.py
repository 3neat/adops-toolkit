import os
from adops import report

def init_reports(folder):
    rpt = []
    for f in os.listdir(folder):
        if f.endswith(".tsv"):
            rpt.append(report.Report(f))
    return rpt



current_directory = os.getcwd()
folder = os.path.join(current_directory, 'reports/')
reports = init_reports(folder)
type = 'Site'
advertiser_id= ['xbci0tw', 'nk6bz6j']

filtered_reports = report.report_filter(reports,type,advertiser_id)


for x in filtered_reports:
    print x.filename