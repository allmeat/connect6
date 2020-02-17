from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql:pymysql//root:allmeat@localhost:3306/playground_log?charset=utf8', convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
