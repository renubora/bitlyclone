from sqlalchemy import create_engine,Table, Column, Integer, ForeignKey,String, Date
from sqlalchemy.orm import scoped_session,sessionmaker,relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

# methods to initalize database and have it up and running 
Base = declarative_base()
engine = create_engine('postgresql+psycopg2://bmcqytfsynajcm:NAkArJX_qEYRk47hOL20uJ4lQZ@ec2-184-72-238-68.compute-1.amazonaws.com/dcif2p4mbqttn2')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50))
    children = relationship("Short")

    def __init__(self,email=None,pwd = None):
        self.name = email
        self.email = email
        self.password = pwd
        

    def __repr__(self):
        return self.name



class Short(Base):
    __tablename__ = 'shorts'
    id = Column(Integer, primary_key=True)
    shorturl = Column(String(50), unique=True)
    longurl = Column(String(120), unique=True)
    created = Column(Date,default=datetime.utcnow)
    created_by = Column(Integer,ForeignKey('user.id'))

    def __init__(self,shorturl, longurl):
        self.shorturl = shorturl
        self.longurl = longurl
        

    def __repr__(self):
        return self.shorturl+' '+self.longurl

    
    