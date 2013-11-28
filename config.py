
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://bmcqytfsynajcm:NAkArJX_qEYRk47hOL20uJ4lQZ@ec2-184-72-238-68.compute-1.amazonaws.com/dcif2p4mbqttn2')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = db_session.query_property()