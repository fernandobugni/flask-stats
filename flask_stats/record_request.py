import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Sequence, Index

Base = declarative_base()


class RecordRequest(Base):
    __tablename__ = 'requests'

    id = Column(Integer, Sequence('request_id_seq'), primary_key=True)
    uri = Column(String(50), index=True)
    response_code = Column(String(50), index=True)
    duration = Column(Float)

    def __repr__(self):
        return "<RecordRequest(uri='%s', response_code='%s', duration='%s')>" % (
                                self.uri, self.response_code, self.duration)
