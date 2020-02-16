from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

"""[reference] https://docs.sqlalchemy.org/en/13/orm/tutorial.html"""

engine = create_engine("mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log", echo=True)

base = declarative_base()

session = sessionmaker(bind=engine)()


# TODO: need dataclass to DB table class converter
class TESTTABLE(base):
    __tablename__ = "TESTTABLE"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


user_list = [
    TESTTABLE(name="glex", age=31),
    TESTTABLE(name="hlex", age=32),
    TESTTABLE(name="ilex", age=33),
]

session.add_all(user_list)

session.commit()
