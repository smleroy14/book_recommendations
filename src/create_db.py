from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import yaml
import pandas as pd
import os
import argparse

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)


Base = declarative_base()

class Book_Recommendations(Base):
    """Create a table of predictions for the database for book recommendations
    """

    __tablename__ = 'Book_Recommendations'

    #User_Picks + Genre will be the composite primary key for the table
    user = Column(String(50), primary_key=True) #will be a string of 1 and 0 that matches the books that the user picked
    genre = Column(String(50), primary_key =True, unique=False, nullable=False) #The genre that the user picks
    author1 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    title1 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended 
    cover1 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    author2 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    title2 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended 
    cover2 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    author3 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    title3 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended 
    cover3 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    author4 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    title4 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended 
    cover4 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended
    author5 = Column(String(200), unique=False, nullable = False) #the book recommendation for the user
    title5 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended 
    cover5 = Column(String(200), unique=False, nullable=False) #the url that will show the picture of the cover of the book recommended

    def __repr__(self):
        recs_repr = "<Book_Recommendations(user='%s', genre = '%s', author1='%s', title1='%s', cover1='%s',  author2='%s', title2='%s', cover2='%s', author3='%s', title3='%s', cover3='%s',  author4='%s', title4='%s', cover4='%s',  author5='%s', title5='%s', cover5='%s')>"
        return recs_repr %(self.user, self.genre, self.author1, self.title1, self.cover1,  self.author2, self.title2, self.cover2, self.author3, self.title3, self.cover3,  self.author4, self.title4, self.cover4, self.author5, self.title5, self.cover5)



class Top_Books(Base):
    """ Creates the table of all the top books by each genre for the user to choose from"""

    __tablename__ = "Top_Books"

    #Book Id will be the primary key for the table
    book_id = Column(Integer, primary_key = True, unique = True, nullable = False) 
    genre = Column(String(50), primary_key = False, unique = False, nullable = False)
    author = Column(String(200), unique = False, nullable = False)
    title = Column(String(200), unique = False, nullable = False)

    def __repr__(self):
        top_books_repr = "<Top_Books(book_id='%d', author='%s', title='%s')>"
        return top_books_repr %(self.book_id, self.author, self.title)


def create_db(SQL_URI=None):
    """Create a database in RDS or locally on sql lite based on user preference"""
    
    if SQL_URI is not None:
        engine_string = SQL_URI
        logger.info(engine_string)
        engine = sql.create_engine(engine_string) 
        Base.metadata.create_all(engine)
        logger.info("Local sqllite database created")
    
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
        logger.info(engine_string)
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("RDS database created")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create database")
    parser.add_argument("--SQL_URI", default=None,
                        help = "If not None, save to sqllite with this URI, else save to RDS db")
    args = parser.parse_args()
    create_db(args.SQL_URI)
