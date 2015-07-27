import os, json
from adops import util


def process_views(views, folder, reports):
    # Iterate through multiple Views within views.json
    # TODO: 1 - Refactor to Views to SQL
    with open(views) as d:
        data = json.load(d)

    for view in data:
        print("Working on: {0}").format(view['name'])
        try:
            util.create_report(folder, reports, view, view["group_by"])
        except ValueError:
            print "ERROR: Improperly formatted views.json"


if __name__ == '__main__':

    # Process Views
    current_directory = os.getcwd()
    folder = os.path.join(current_directory, 'reports/')
    reports = util.init_reports(folder)
    process_views('views.json', folder, reports)