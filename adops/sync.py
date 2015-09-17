from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

def importer(engine, reports, reporttype, tablename):
    Base = declarative_base()
    engine = create_engine(engine)
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    for report in reports:
        print report.filename

