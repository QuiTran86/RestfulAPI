from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from RestfulAPI.config import Config


class UsersPG:

    def __init__(self):
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        session = sessionmaker(bind=engine)
        self.session = session()

    def store_account(self, account):
        try:
            self.session.add(account)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
