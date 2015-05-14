import os
from adops import report

def init_reports(folder):
    reports_list = []
    for f in os.listdir(folder):
        if f.endswith(".tsv"):
            reports_list.append(report.Report(f))
    return reports_list



current_directory = os.getcwd()
folder = os.path.join(current_directory, 'reports/')
reports = init_reports(folder)
