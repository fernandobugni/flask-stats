from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_stats.record_request import RecordRequest, Base
from sqlalchemy.sql import func
from sqlalchemy.sql import label

MAX_NUMBER_ROWS = 6


class SqliteRepository:

    def __init__(self, database_name='.example'):
        self.engine = create_engine('sqlite:///%s.db' % database_name, echo=True)
        self.session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        trigger_drop = "DROP TRIGGER IF EXISTS request_limiter;"
        self.engine.execute(trigger_drop)
        trigger = '''
                CREATE TRIGGER request_limiter AFTER INSERT ON requests
                BEGIN
                    DELETE FROM requests WHERE id NOT IN 
                        (SELECT  id FROM requests ORDER BY id DESC limit %s);
                END
                ''' % MAX_NUMBER_ROWS
        self.engine.execute(trigger)

    def save_request(self, request: RecordRequest):
        session = self.session()
        session.add(request)
        session.commit()

    def get_requests_stats(self):
        session = self.session()
        return session.query(RecordRequest).filter(RecordRequest.uri.is_('/stats')).order_by(
            RecordRequest.duration).all()

    def get_requests(self):
        session = self.session()
        query = session.query(RecordRequest,
                              label('uri', RecordRequest.uri),
                              label('min', func.min(RecordRequest.duration)),
                              label('max', func.max(RecordRequest.duration)),
                              label('avg', func.avg(RecordRequest.duration)),
                              label('count', func.count(RecordRequest.duration)))
        result_list = query.group_by(RecordRequest.uri).all()
        return [{"endpoint \"" + x[1] + "\" ": {'min': x[2], 'max': x[3], 'avg': x[4], 'count': x[5],
                                                'percentile_25': self.get_request_percentile(uri=x[1], percentile=2.5),
                                                'percentile_50': self.get_request_percentile(uri=x[1], percentile=5),
                                                'percentile_75': self.get_request_percentile(uri=x[1], percentile=7.5),
                                                'percentile_90': self.get_request_percentile(uri=x[1], percentile=9)
                                                }
                 } for x in result_list]

    def get_request_percentile(self, uri='/', percentile=9):
        session = self.session()
        query_count = session.query(RecordRequest).filter(RecordRequest.uri.is_(uri)).count()
        offset = (query_count * percentile) / 10
        query = session.query(RecordRequest, RecordRequest.duration) \
            .filter(RecordRequest.uri.is_(uri)) \
            .order_by(RecordRequest.uri.asc()).limit(1).offset(offset - 1)
        result = query.all()
        return result[0][1]
