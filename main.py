import os, json
from adops import report, util


def init_reports(folder):
    rpt = []
    for f in os.listdir(folder):
        if f.endswith(".tsv"):
            report_type = get_report_type(f)

            if report_type == 'Site':
                rpt.append(report.SiteReport(os.path.join(folder, f)))
            if report_type == 'Site List':
                rpt.append(report.SiteListReport(os.path.join(folder, f)))
            if report_type == 'Data Element Report':
                rpt.append(report.DataElementReport(os.path.join(folder, f)))
            if report_type == 'Time of Day':
                rpt.append(report.TimeOfDayReport(os.path.join(folder, f)))
            if report_type == 'Browser Report':
                rpt.append(report.BrowserReport(os.path.join(folder, f)))
            if report_type == 'Ad Group Recency':
                rpt.append(report.AdGroupRecencyReport(os.path.join(folder, f)))
            if report_type == 'Performance':
                rpt.append(report.PerformanceReport(os.path.join(folder, f)))
            if report_type == 'Geo Report':
                rpt.append(report.GeoReport(os.path.join(folder, f)))
            if report_type == 'Conversions':
                print "Ignoring Conversions Report"
    return rpt

def get_report_type(filename):
    file_info = report.parse_filename(filename)
    return file_info['report_type']

def main():
    current_directory = os.getcwd()
    folder = os.path.join(current_directory, 'reports/')
    reports = init_reports(folder)

    # Iterate through multiple Views within views.json
    # TODO: 1 - Refactor to Views to SQL

    with open('views.json') as d:
        data = json.load(d)

    for view in data:
        print("Working on: {0}").format(view['name'])
        try:
            util.create_report(folder, reports, view, view["group_by"])
        except ValueError:
            print "ERROR: Improperly formatted views.json"

if __name__ == '__main__':
    main()