from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import yaml
import pandas as pd
import os
import sys

with open("config.yml", "r") as f:
    config = yaml.load(f)

# set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

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


def create_db(conn_type, user, password, host, port, DATABASE_NAME):
    """Creates an RDS database using dbconfig with Book_Recommendations table"""
    
    engine_string = "{}://{}:{}@{}:{}/{}".\
    format(conn_type, user, password, host, port, DATABASE_NAME)
    logger.info(engine_string)
    engine = sql.create_engine(engine_string)
    Base.metadata.create_all(engine)
    logger.info("Creating RDS database")


def add_to_db(conn_type, user, password, host, port, DATABASE_NAME, user_pick, genre, book_rec, book_cover):
    
    engine_string = "{}://{}:{}@{}:{}/{}".\
    format(conn_type, user, password, host, port, DATABASE_NAME)
    logger.info(engine_string)
    engine = sql.create_engine(engine_string)
    Session = sessionmaker(bind=engine)  
    session = Session()
    book_rec =  Book_Recommendations(User_Pick = user_pick, Genre= genre, Book_Recommendation= book_rec, Book_Cover = book_cover)
    session.add(book_rec)
    session.commit()
    logger.info("Added book recommendation to database: " + book_rec)  
    session.close()
    
