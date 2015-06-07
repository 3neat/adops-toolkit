import os, json
from adops import report, util


def init_reports(folder):
    # TODO: 3 - May want to consider refactoring this to pass entire path; verify for cross OS compatibility
    rpt = []
    for f in os.listdir(folder):
        if f.endswith(".tsv"):
            rpt.append(report.Report(os.path.join(folder, f)))
    return rpt


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
            util.create_report(folder, reports, view)
        except ValueError:
            print "ERROR: Improperly formatted views.json"


if __name__ == '__main__':
    main()