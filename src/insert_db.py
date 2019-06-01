import pandas as pd
import os
from schema import Book_Recommendations
from db_conn import dbConn

def read_recs():
    """ Takes the predictions for the new users and merges with the book cover picture url"""


def insert_data(sqllite=True):
    recs_df = read_recs()

    #if sqllite = True, do it
    if sqllite:
        #something
        # conn = dbConn('../../data/song.sqlite')
        # song_df.to_sql(name='Song', con=conn, if_exists='replace', index=True)
    
    #If False, insert to RDS database
    else:
        #song_df.to_sql("Song", db.engine, if_exists='replace', index=False)
                

if __name__=='__main__':
    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['insert_db']

    insert_data(**config_try['insert_data'])

