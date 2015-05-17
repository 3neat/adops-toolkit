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


def report_filter(reports, type, advertiser_id=None, date_range=None):
    # TODO: 2 - Refactor filter using generators or decorator based on that one book

    # Filter reports by: Type
    rpt = []
    [rpt.append(f) for f in reports if f.report_type == type]

    # Filter reports by: Advertiser
    filtered_list = []
    if advertiser_id:
        # Make sure that advertiser_id is a list
        if isinstance(advertiser_id, basestring):
            advertiser_id = list([advertiser_id])

        for r in rpt:
            if r.advertiser_id in advertiser_id:
                filtered_list.append(r)
    else:
        filtered_list = rpt

    # Filter reports by: Date Range
    last_filtered_list = []
    if date_range:
        for r in filtered_list:
            now = datetime.now()
            delta = now - r.end_date

            if int(delta.days) <= date_range:
                # TODO: This should eventually become the basis of logging
                # print r.filename + " " + str(delta.days)
                last_filtered_list.append(r)
    return last_filtered_list