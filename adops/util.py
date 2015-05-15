import pandas as pd
from os import path


def combine_reports(files, columns, folder):
    # Return an aggregate DataFrame for a given set of files

    section = pd.DataFrame()

    for rpt in files:
        report_path = str(path.join(folder, rpt.filename))
        df = pd.read_csv(report_path,
                         usecols=columns,
                         sep='\t')
        section = pd.concat([section, df])
    return section

