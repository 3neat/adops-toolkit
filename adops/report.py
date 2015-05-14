from os import path


class Report(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = path.basename(self.filepath)