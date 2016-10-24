import pandas as pd
import numpy as np
from os import listdir, path
from adops import report

def init_reports(folder):
    rpt = []
    for f in listdir(folder):
        if f.endswith(".tsv"):
            report_type = get_report_type(f)

            if report_type == 'Site':
                rpt.append(report.SiteReport(path.join(folder, f)))
            if report_type == 'Site List':
                rpt.append(report.SiteListReport(path.join(folder, f)))
            if report_type == 'Data Element Report':
                rpt.append(report.DataElementReport(path.join(folder, f)))
            if report_type == 'Time of Day':
                rpt.append(report.TimeOfDayReport(path.join(folder, f)))
            if report_type == 'Browser Report':
                rpt.append(report.BrowserReport(path.join(folder, f)))
            if report_type == 'Ad Group Recency':
                rpt.append(report.AdGroupRecencyReport(path.join(folder, f)))
            if report_type == 'Performance':
                rpt.append(report.PerformanceReport(path.join(folder, f)))
            if report_type == 'Geo Report':
                rpt.append(report.GeoReport(path.join(folder, f)))
            if report_type == 'Conversions':
                rpt.append(report.ConversionReport(path.join(folder, f)))
    return rpt


def get_report_type(filename):
    file_info = report.parse_filename(filename)
    return file_info['report_type']


def adgroup_filter(df, adgroups):
    # isinstance() let's us take in either a string or a list
    if isinstance(adgroups, basestring):
        df = df[df['adgroup_id'].isin([adgroups])]
    else:
        df = df[df['adgroup_id'].isin(adgroups)]
    return df


def campaign_filter(df, campaign_id):
    # isinstance() let's us take in either a string or a list
    if isinstance(campaign_id, basestring):
        df = df[df['campaign_id'].isin([campaign_id])]
    else:
        df = df[df['campaign_id'].isin(campaign_id)]

    return df


def combine_reports(reports, view=None):
    # Return an aggregate DataFrame for a given set of files
    section = pd.DataFrame()

    for rpt in reports:
        df = rpt.to_df(rename_cols=True)

        if view["campaign"]:
            df = campaign_filter(df, view["campaign"])


        if view["adgroup"]:
            df = adgroup_filter(df, view["adgroup"])

        section = pd.concat([section, df])

    return section


def add_metrics(df):
    # Add common metrics to DataFrame
    df['ctr'] = df.clicks / df.impressions
    df['win_rate'] = df.impressions / df.bids
    df['avg_bid'] = df.bid_amount / df.bids * 1000
    df['tc'] = df.ctc_1 + df.vtc_1 + df.ctc_2 + df.vtc_2 + df.ctc_3 + df.vtc_3 + df.ctc_4 + df.vtc_4 + df.ctc_5 + df.vtc_5
    df['ecpc'] = df.cost / df.clicks
    df['ecpm'] = df.cost / df.impressions * 1000
    df['ecpa'] = df.cost / df.tc
    df['moat'] = df.creative_was_viewable / df.creative_is_trackable

    # TEMP: Delete raw numbers
    df.drop('bid_amount', axis=1, inplace=True)
    df.drop('creative_is_trackable', axis=1, inplace=True)
    df.drop('creative_was_viewable', axis=1, inplace=True)
    return df


def rules_filter(df, rules):
    t = pd.DataFrame()
    for rule in rules:
        t = pd.concat([t, df.query(rule)])
    t.drop_duplicates(inplace=True)
    return t


def format_excel(df, filename, sheetname="1"):
    # ERROR IS IN HERE WHEN TO XLSX IS RUNNING
    # TODO: Place a file extension check to ensure one .xlsx

    # TODO: Sort DataFrame by 'cost' DESC
    df.sort('cost')

    filename = ''.join([filename, ".xlsx"])
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheetname)

    workbook = writer.book
    worksheet = writer.sheets[sheetname]

    currency = workbook.add_format({'num_format': '$#,###.##'})
    percentage = workbook.add_format({'num_format': '0.00%'})

    worksheet.set_column('A:A', 55)
    worksheet.set_column('Q:Q', None, currency)
    worksheet.set_column('T:T', None, currency)
    worksheet.set_column('V:V', None, currency)
    worksheet.set_column('W:W', None, currency)
    worksheet.set_column('X:X', None, currency)

    worksheet.set_column('R:R', None, percentage)
    worksheet.set_column('S:S', None, percentage)
    worksheet.set_column('Y:Y', None, percentage)

    writer.save()


def create_report(folder, reports, view, group_by):
    # Filter out the needed report files for analysis
    filtered_reports = report.report_filter(reports, **view)

    # Transform report files to working DataFrame
    # TODO: 1.a - Refactor this out so that it uses report.filepath instead
    df = combine_reports(filtered_reports, view)

    df = df.groupby(view["group_by"])

    # Quick hack by taking the first report's renamed column attribute to sum up values
    columns = filtered_reports[0].rn_columns
    df = df[[x for x in columns]].aggregate(np.sum)

    df = add_metrics(df)


    if view['rules']:
        df = rules_filter(df, view['rules'])

    # Save to CSV:
    #df.to_csv(''.join([view['name'], '.csv']))

    # Save to formatted XLSX:
    format_excel(df, view['name'])

