import os, sys, json
import datetime
from adops import util, downloader
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

def download_reports(date):
    # Given a start date, download all 7 day report files, from all advertisers

    # Make sure the provided date is in the correct format
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect date usage, should be YYYY-MM-DD")

    report_time = ''.join([date, ' 14:00:44.092598+00:00'])
    token = settings["ttd"]["token"]
    ttd = downloader.TTD(token)

    print ttd.get_advertisers()




if __name__ == '__main__':
    # We'll stop using sys.argv once download() is implemented
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'process':
            process_views()
        if command == 'download' and sys.argv[2]:
            # completely assumes that date is passed in as second argument in yyyy-mm-dd format
            date = sys.argv[2]
            download_reports(date)
        else:
            print "Command not found: python main.py process|download (date)"
    else:
        print "Not enough arguments: python main.py process|download (date)"