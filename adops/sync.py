from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
import pandas as pd
import datetime




Base = declarative_base()

class Processed(Base):
    __tablename__ = 'processed'

    id = Column(Integer, primary_key=True)
    filehash = Column(String)
    filename = Column(String)
    row_count = Column(Integer)
    date_processed = Column(DateTime)
    report_type = Column(String)
    advertiser_name = Column(String)
    report_start_date = Column(DateTime)
    report_end_date = Column(DateTime)

    def __repr__(self):
        return "<File(%r)" % (self.filename)


def append_column(df, value):
    row_count = df.shape[0]
    rows = []
    for x in xrange(row_count):
        rows.append(value)
    return rows

def importer(engine, reports, reporttype, tablename):
    engine = create_engine(engine)
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    for report in reports:
        filehash = report.githash()

        if session.query(exists().where(Processed.filehash == filehash)).scalar():
            #print "already processed %s" % (report.filename)
            pass
        else:
            df = pd.DataFrame()
            df = report.to_df(rename_cols=True)
            #print "Working on: %s" % report.filename

            # Append Report Start Date:
            ser = append_column(df,report.start_date)
            start_series = pd.to_datetime(pd.Series(ser, name="report_start_date"))
            tmp_df = pd.concat([df, start_series], axis=1)

            # Append Report End Date:
            ser = append_column(df,report.end_date)
            end_series = pd.to_datetime(pd.Series(ser, name="report_end_date"))
            df = pd.concat([tmp_df, end_series], axis=1)

            # Append Filehash:
            ser = append_column(df,filehash)
            end_series = pd.to_datetime(pd.Series(ser, name="filehash"))
            df = pd.concat([tmp_df, end_series], axis=1)


            rows = len(df.index)
            date_processed = datetime.datetime.now()

            # DataFrame to SQL
            df.to_sql(tablename, engine, if_exists='append', dtype=report.dtype, index=False)
            print "Inserting %s rows for file: %s" % (rows, report.filename)
            # try:
            #     df.to_sql(tablename, engine, if_exists='append', dtype=report.dtype, index=False)
            #     print "Inserting %s rows for file: %s" % (rows, report.filename)
            # except:
            #     print "*** ERROR importing: %s" % report.filename


            process_transaction = Processed(filehash=filehash, filename=report.filename, row_count=rows,
                                            date_processed=date_processed, report_type=report.report_type,
                                            advertiser_name=report.advertiser, report_start_date=report.start_date,
                                            report_end_date=report.end_date)
            session.add(process_transaction)
            session.commit()
            #print "Done importing %s into %s" % (reporttype, tablename)
