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

def read_recs(genre_csv, genre, books_csv):
	""" Takes the predictions for the new users and merges with the book cover picture url"""
	recs = pd.read_csv(genre_csv)
	recs_melt = pd.melt(recs, id_vars =['user'], value_vars =['book1', 'book2', 'book3', 'book4', 'book5'])
	recs_melt.columns = ['user', 'rec_no', 'book_id']
	books = pd.read_csv(books_csv)
	books = books[['book_id', 'image_url', 'authors', 'original_title']]
	merged = pd.merge(recs_melt, books, how='left', on='book_id')
	recs_for_db = merged.pivot(index='user', columns='rec_no', values=['book_id', 'image_url', 'authors', 'original_title'])
	recs_for_db.columns = recs_for_db.columns.droplevel(0)
	recs_for_db = recs_for_db.reset_index().rename_axis(None, axis=1)
	recs_for_db.columns = ['user', '1', '2', '3' ,'4', '5', 'cover1', 'cover2', 'cover3' ,'cover4', 'cover5', 'author1', 'author2', 'author3' ,'author4', 'author5', 'title1', 'title2', 'title3' ,'title4', 'title5']
	recs_for_db = recs_for_db[['user', 'cover1', 'cover2', 'cover3' ,'cover4', 'cover5', 'author1', 'author2', 'author3' ,'author4', 'author5', 'title1', 'title2', 'title3' ,'title4', 'title5']]
	recs_for_db['genre'] = genre
	logger.info(recs_for_db.head())
	return recs_for_db

def get_top_books(genre):
    data = pd.read_pickle(genre_pickle_file)
    data = data[['user_id','book_id','rating']]

    #get top books for choices
    top_books = data.groupby(['book_id']).count().reset_index()
    top_books = top_books[['book_id']]
    top_books = top_books.head(num_choices)

    #sort on book id, so combos are always in increasing order for user_id
    top_books = top_books.sort_values('book_id', ascending = True).reset_index()
    top_books[['book_id']]
    
    #merge on books to get author and title
    top_books = pd.merge(top_books, books, how='left', on='book_id')
    top_books = top_books[['book_id','authors', 'original_title']]
    top_books.columns = ['book_id', 'author', 'title']
    return top_books


def add_data(df, table_name, SQL_URI=None):

    #if sqllite = True, add df to local SQLlite database
    if SQL_URI:
        engine_string = SQL_URI
        engine = sql.create_engine(engine_string)
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=True)
	    
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
                

if __name__=='__main__':
	with open("config.yml", "r") as f:
		config = yaml.load(f)
	config_try = config['insert_db']

	recs_for_db = read_recs(**config_try['read_recs'])
	print(recs_for_db.head())
	add_data(recs_for_db, 'Book_Recommendations')
        add_data(top_books, 'Top_Books')
