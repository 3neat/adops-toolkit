from os import path
from datetime import datetime
import re


class Report(object):
    def _parse_filename(self, filename):
        # Parse the filename for all metadata
        regex = re.compile(r'.*Advertiser - (?P<advertiser>.*) - (?P<advertiser_id>\w{7}) - (RTB )?(?P<report_type>.*) - '
                           r'(?P<report_length>\d{1,2} Days) - USD - (?P<report_start_date>\d{8})-'
                           r'(?P<report_end_date>\d{8})\.tsv$')

        match = regex.match(self.filename)
        if match:
            file_info = match.groupdict()
            file_info['filename'] = self.filename
            file_info['report_start_date'] = datetime.strptime(file_info['report_start_date'], '%Y%m%d')
            file_info['report_end_date'] = datetime.strptime(file_info['report_end_date'], '%Y%m%d')
            return file_info
        else:
            print "Unexpected file type or name: " + self.filename


    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = path.basename(self.filepath)

        tmp = self._parse_filename(self.filename)
        self.report_type = tmp['report_type']
        self.start_date = tmp['report_start_date']
        self.end_date = tmp['report_end_date']
        self.report_length = tmp['report_length']
        self.advertiser = tmp['advertiser']
        self.advertiser_id = tmp['advertiser_id']


def report_filter(reports, **view):
    # TODO: 2 - Refactor filter using generators or decorator based on that one book
    # TODO: 1 - Implement unit testing for this function

    # Filter reports by: Type
    reports = [r for r in reports if r.report_type == view['report_type']]

    # Filter reports by: Advertiser
    if view['advertiser'] is not None:
        reports = [r for r in reports if r.advertiser_id in view['advertiser']]

    # Filter reports by: Date Range
    filtered_list = []
    if view['date_range'] is not None:
        for r in reports:
            now = datetime.now()
            delta = now - r.end_date

            if int(delta.days) <= view['date_range']:
                # TODO: 3 - This should eventually become the basis of logging
                # print r.filename + " " + str(delta.days)
                filtered_list.append(r)

        reports = filtered_list
    return reports