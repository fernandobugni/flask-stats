from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_stats.record_request import RecordRequest, Base

MAX_NUMBER_ROWS = 6


class SqliteRepository:

    def __init__(self, database_name = '.example'):

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

    def get_requests(self):
        session = self.session()
        return session.query(RecordRequest).filter(RecordRequest.uri.is_('/stats')).order_by(RecordRequest.duration).all()

