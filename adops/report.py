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