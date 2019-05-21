from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os
import argparse

# set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

def str2bool(v):
   if v.lower() in ('yes', 'true', 't', 'y', '1'):
       return True
   elif v.lower() in ('no', 'false', 'f', 'n', '0'):
       return False
   else:
       raise argparse.ArgumentTypeError('Boolean value expected.')
   
Base = declarative_base()

class Book_Recommendations(Base):
    """Create a table of predictions for the database for book recommendations
    """

    __tablename__ = 'Book_Recommendations'

    #User_Picks + Genre will be the composite primary key for the table
    User_Picks = Column(String(50), primary_key=True) #will be a string of 1 and 0 that matches the books that the user picked
    Genre = Column(String(50), primary_key =True, unique=False, nullable=False) #The genre that the user picks
    Book_Recommendation = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    Book_Cover = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended

    def __repr__(self):
        return '<Book_Recommendations %r>' % self.Book_Cover

def create_db(RDS):
    """Create a database in RDS or locally on sql lite based on user preference"""
    
    if RDS == True:
        #get configurations from .mysqlconfig
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER") 
        password =  os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST") 
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = os.environ.get("DATABASE_NAME")

        # the engine_string format
        #engine_string = "{conn_type}://{user}:{password}@{host}:{port}/DATABASE_NAME"
        engine_string = "{}://{}:{}@{}:{}/{}".\
        format(conn_type, user, password, host, port, DATABASE_NAME)
        print(engine_string)
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
    else:
        SQL_URI = "sqlite:///data/database.db"
        engine_string = SQL_URI
        engine = sql.create_engine(engine_string) 
        Base.metadata.create_all(engine)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create database")
    parser.add_argument('--rds', default=True, type=str2bool, help='True to create RDS database, False creates sqllite database')
    args = parser.parse_args()
    create_db(args.rds)


def add_to_RDS_db(user_pick, genre, book_rec, book_cover):

    #get configurations from .mysqlconfig
    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER") 
    password =  os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST") 
    port = os.environ.get("MYSQL_PORT")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    
    format(conn_type, user, password, host, port, DATABASE_NAME)
    # the engine_string format
    #engine_string = "{conn_type}://{user}:{password}@{host}:{port}/DATABASE_NAME"
    engine_string = "{}://{}:{}@{}:{}/{}".\
    logger.info(engine_string)
    engine = sql.create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    book_rec =  Book_Recommendations(User_Pick = user_pick, Genre= genre, Book_Recommendation= book_rec, Book_Cover = book_cover)
    session.add(book_rec)
    session.commit()
    logger.info("Added book recommendation to database: " + book_rec)
    session.close()


