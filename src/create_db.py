from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os
import argparse

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
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
    user_id = Column(String(50), primary_key=True) #will be a string of 1 and 0 that matches the books that the user picked
    Genre = Column(String(50), primary_key =True, unique=False, nullable=False) #The genre that the user picks
    book_rec1 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    book_cover1 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    book_rec2 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    book_cover2 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    book_rec3 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    book_cover3 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    book_rec4 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    book_cover4 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    book_rec5 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    book_cover5 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended

    def __repr__(self):
        return '<Book_Recommendations %r>' % self.Book_Cover

def create_db(sqllite = True):
    """Create a database in RDS or locally on sql lite based on user preference"""
    
    if sqllite = True:
        SQL_URI = "sqlite:///data/database.db"
        engine_string = SQL_URI
        engine = sql.create_engine(engine_string) 
        Base.metadata.create_all(engine)
    
    else:
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


if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['create_db']

    create_db(**config_try['create_db'])

    parser = argparse.ArgumentParser(description="Create database")
    parser.add_argument('--rds', default=True, type=str2bool, help='True to create RDS database, False creates sqllite database')
    args = parser.parse_args()
    create_db(args.rds)
