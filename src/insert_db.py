import pandas as pd
import os
from create_db import Book_Recommendations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sql
import logging
import yaml
import argparse


#Logging file
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

def read_recs(df, books_csv):
    """ Takes the predictions for the new users and merges with the book cover picture url"""
    recs = df
    recs_melt = pd.melt(recs, id_vars =['user', 'genre'], value_vars =['book1', 'book2', 'book3', 'book4', 'book5'])
    recs_melt.columns = ['user', 'genre', 'rec_no', 'book_id']
    books = pd.read_csv(books_csv)
    books = books[['book_id', 'image_url', 'authors', 'title']]
    merged = pd.merge(recs_melt, books, how='left', on='book_id')
    recs_for_db = merged.pivot(index='user', columns='rec_no', values=['genre', 'book_id', 'image_url', 'authors', 'title'])
    recs_for_db.columns = recs_for_db.columns.droplevel(0)
    recs_for_db = recs_for_db.reset_index().rename_axis(None, axis=1)
    recs_for_db.columns = ['user', 'genre1', 'genre2', 'genre3', 'genre4', 'genre5', '1', '2', '3' ,'4', '5', 'cover1', 'cover2', 'cover3' ,'cover4', 'cover5', 'author1', 'author2', 'author3' ,'author4', 'author5', 'title1', 'title2', 'title3' ,'title4', 'title5']
    recs_for_db = recs_for_db[['user', 'genre1', 'cover1', 'cover2', 'cover3' ,'cover4', 'cover5', 'author1', 'author2', 'author3' ,'author4', 'author5', 'title1', 'title2', 'title3' ,'title4', 'title5']]
    recs_for_db.rename(columns={'genre1':'genre'}, inplace=True)
    logger.info(recs_for_db.head())
    return recs_for_db

def get_top_books(df, num_choices, books_csv):
    data = df
    data = data[['user_id','genre', 'book_id','rating']]

    #get top books for choices
    top_books = data.groupby(['book_id', 'genre']).count().reset_index()
    top_books = top_books.groupby('genre').head(num_choices).reset_index(drop=True)
    top_books = top_books[['book_id', 'genre']]

    #sort on book id, so combos are always in increasing order for user_id
    top_books = top_books.sort_values('book_id', ascending = True).reset_index()
    top_books[['book_id', 'genre']]
    
    #merge on books to get author and title
    books = pd.read_csv(books_csv)

    top_books = pd.merge(top_books, books, how='left', on='book_id')
    top_books = top_books[['book_id','genre', 'authors', 'title']]
    top_books.columns = ['book_id', 'genre', 'author', 'title']
    logger.info(top_books.head())
    return top_books


def add_data(df, table_name, SQL_URI=None):

    #if sqllite = True, add df to local SQLlite database
    if SQL_URI:
        engine_string = SQL_URI
        engine = sql.create_engine(engine_string)
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=True)
        logger.info("Data inserted into %s", table_name)
	    
    #If False, add df to RDS database
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
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info("Data inserted into %s", table_name)
                

def run_insert_db(args):
    with open(args.config, "r") as f:
        config = yaml.load(f)
        config_try = config['insert_db']

    if args.input is not None:
        df = pd.read_csv(args.input)
        logger.info("Features for input into database loaded from %s", args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")

    if args.table == "Book_Recommendations":
        recs_for_db = read_recs(df, **config_try['read_recs'])
        logger.info("recs added to Book_Recommendations table")
        logger.info(recs_for_db.head())
        add_data(recs_for_db, 'Book_Recommendations', args.SQL_URI)
    elif args.table == "Top_Books":
        top_books = get_top_books(df, **config_try['get_top_books'])
        add_data(top_books, 'Top_Books', args.SQL_URI)
        logger.info("top books added to Top_Books table")
        logger.info(top_books.head())
    else:
        raise ValueError("%s is not a valid table name", args.table)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Store data in database")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="data/recs/all_recs.csv",
                        help="Path to input data for storing in database")
    parser.add_argument("--table", "-o",  default="Book_Recommendations",
                        help="Name of Table in database to save data")
    parser.add_argument("--SQL_URI", default = None, 
			help = "If not None, save to sqllite with this URI, else save to RDS db")
    args = parser.parse_args()

    run_insert_db(args)

