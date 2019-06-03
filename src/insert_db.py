import pandas as pd
import os
#from schema import Book_Recommendations

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

#def insert_data(sqllite=True):
#	recs_df = read_recs()

#	#if sqllite = True, do it
#	if sqllite:
#		#something
#		# conn = dbConn('../../data/song.sqlite')
#		# song_df.to_sql(name='Song', con=conn, if_exists='replace', index=True)
	    
#	#If False, insert to RDS database
#	else:
#		#song_df.to_sql("Song", db.engine, if_exists='replace', index=False)
                

if __name__=='__main__':
	with open("config.yml", "r") as f:
		config = yaml.load(f)
	config_try = config['insert_db']

	recs_for_db = read_recs(**config_try['read_recs'])
	print(recs_for_db.head())
	#insert_data(**config_try['insert_data'])

