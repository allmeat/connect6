from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session

"""[reference] https://docs.sqlalchemy.org/en/13/orm/tutorial.html"""


class DBConfig:

    def __init__(self):
        super(DBConfig, self).__init__()
        self.session_maker = sessionmaker()

    def setup_db_connection(self, uri, echo=False) -> Session:
        engine = create_engine(uri, echo=echo)
        self.session_maker.configure(bind=engine)
        session = self.session_maker()
        return session

    @staticmethod
    def insert(session, item):
        session.add(item)
        session.commit()

    @staticmethod
    def insert_list(session, item_list):
        session.add_all(item_list)
        session.commit()


if __name__ == "__main__":
    base = declarative_base()


    class TESTTABLE(base):
        __tablename__ = "TESTTABLE"

        id = Column(Integer, primary_key=True)
        name = Column(String)
        age = Column(Integer)

    user_list = [
        TESTTABLE(name="mlex", age=31),
        TESTTABLE(name="nlex", age=32),
        TESTTABLE(name="olex", age=33),
    ]

    db = DBConfig()
    sess = db.setup_db_connection("mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log")
    db.insert(sess, user_list[0])
    # db.insert_list(sess, user_list)

    print("insert done")
