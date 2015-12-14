import os, sys, json, re
import datetime, urllib
from adops import util, downloader, sync
from config import settings


p = re.compile(".*7days/(.*)\?")

def get_report_url(reports):
    # Iterate through all Advertiser's reports JSON responses for a specific start date
    urls = []
    for report in reports["Result"]:
        # Iterating through the Advertisers...

        if report["Duration"] == "SevenDays" and report["Scope"] == "Advertiser":
            # This limits to Seven Day reports, but can be passed in through as a variable
            # in future refactoring... then download 1 day, 30 days, MTDs.

            if report["Type"] != "ExcelPivotReports":
                # Ignore ExcelPivot Reports
                urls.append(report['DownloadUrl'])

    # TODO: Add in check to see if Report Results = 8 OR 9 and to discard 0 or 1-7
    return urls


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
    ttd = downloader.TTDConnection(token)

    all_reports = ttd.get_reports(report_time)

    # Get Report URLs
    urls = []
    for advertiser in all_reports:
        urls.append(get_report_url(json.loads(advertiser.text)))

    # Download the reports
    for url in urls:
        for u in url:
            try:
                filename = p.match(u).groups()[0]
                filename = urllib.unquote(filename).decode('utf8')
                print "Downloading: %s" % filename
                testfile = urllib.URLopener()
                testfile.retrieve(u,filename)
            except:
                print "Error download: %s" % u


def sync_to_db(engine, reporttype, tablename):
    report_folder = settings["report_folder"]
    current_directory = os.getcwd()
    folder = os.path.join(current_directory, report_folder)
    reports = util.init_reports(folder)
    filtered_reports = []

    for rpt in reports:
        if rpt.report_type == reporttype:
            filtered_reports.append(rpt)

    sync.importer(engine, filtered_reports, reporttype, tablename)
    print "** importing to DB"


def to_sql():
    import_combos = zip(["Site",
                     "Site List",
                     "Data Element Report",
                     "Time of Day",
                     "Performance",
                     "Geo Report",
                     "Browser Report",
                     "Conversions"],
                    ["sites",
                     "site_lists",
                     "data_elements",
                     "time_of_day",
                     "performance",
                     "geography",
                     "browsers",
                     "conversions"])

    engine = settings["db_engine"]

    for combo in import_combos:
        reporttype, tablename = combo
        print "* Starting to import %s    -->     %s" % (reporttype, tablename)
        sync_to_db(engine, reporttype, tablename)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        process_views()

    # We'll stop using sys.argv once download() is implemented
    elif len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'process':
            # This will process rules against views.json
            # python main.py process
            process_views()
        if command == 'download' and sys.argv[2]:
            # This will download all 7 day reports from a provided date 'yyyy-mm-dd' format
            # python main.py download 2015-09-09
            date = sys.argv[2]
            download_reports(date)
        if command == 'sync':
            # This will sync new report files to the database
            # python main.py sync
            to_sql()
        else:
            print "Command not found: python main.py process | download (date) | sync"
    else:
        print "This shouldn't be firing..."