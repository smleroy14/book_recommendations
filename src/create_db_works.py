from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os

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

# the engine_string format
#engine_string = "{conn_type}://{user}:{password}@{host}:{port}/DATABASE_NAME"
conn_type = "mysql+pymysql"
user = "root"
password = "avc_project"
host = "mysql-avc-app-michel.cmq30xngrjmp.us-east-2.rds.amazonaws.com"
port = 3306
DATABASE_NAME = 'msia423'
engine_string = "{}://{}:{}@{}:{}/{}".\
format(conn_type, user, password, host, port, DATABASE_NAME)
#print(engine_string)
engine = sql.create_engine(engine_string)
Base.metadata.create_all(engine)

# set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)
# create a db session
Session = sessionmaker(bind=engine)  
session = Session()

# add a book_rec
book_rec1 = Book_Recommendations(User_Picks="1010101", Genre="YA", Book_Recommendation="Harry Potter 2", Book_Cover = "thiswillbeaurl")  
session.add(book_rec1)
session.commit()
logger.info("Database created with book recommendation added: Harry Potter")  
book_record = session.query(Book_Recommendations.Genre, Book_Recommendations.Book_Recommendation).filter_by(User_Picks="101010").first()
print(book_record)
query = "SELECT * FROM Book_Recommendations WHERE Book_Recommendation LIKE '%%Harry%%'"
df = pd.read_sql(query, con=engine)
print(df)
session.close()
