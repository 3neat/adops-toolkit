import os, sys, json
from adops import util
from config import settings



def process_views():
    try:
        folder = os.path.join(os.getcwd(), settings['report_folder'])
        views = settings['views_file']
        reports = util.init_reports(folder)
    except:
        print "reports folder not found. please set in settings.yaml and ensure it's present"

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
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'process':
            process_views()
        else:
            print "Command not found: python main.py process "
    else:
        print "Not enough arguments: python main.py process"