import random
import pandas as pd

#from surprise import Dataset
#from surprise import Reader
#from surprise import SVD, KNNBasic, KNNWithMeans, KNNWithZScore
#from surprise import accuracy
#from surprise.model_selection import KFold
#from surprise.model_selection import GridSearchCV

from collections import defaultdict
import itertools 

import logging
import yaml
import argparse


#Logging file
    
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)


def get_combo_df(genre_pickle_file):
    """ Iterates through the top 20 books of a genre and
    gets all combinations of choosing 3 of these
    
    Returns a dataframe of "users" with 5 ratings for the 
    books they chose
    """

    data = pd.read_pickle(genre_pickle_file)
    data = data[['user_id','book_id','rating']]

    #get top 20 books
    top_books = data.groupby(['book_id']).count().reset_index()
    top_books = top_books[['book_id']]
    top_books = top_books.head(20)
    
    #sort on book id, so combos are always in increasing order for user_id 
    top_books = top_books.sort_values('book_id', ascending = True).reset_index()
    top_books[['book_id']]

    #convert these to a list
    top_for_combo = []
    for i in range(len(top_books)):
         top_for_combo.append(top_books['book_id'][i])

    #iterate through the top list to get all possible combinations
    combos = itertools.combinations(top_for_combo, 3)
    combos = list(combos)
    combos_df = pd.DataFrame(combos, columns=['book1', 'book2', 'book3'])

    #set the combo of three top picks as user id
    combos_df['user_id']=combos_df['book1'].astype(str)+', '+combos_df['book2'].astype(str)+', '+combos_df['book3'].astype(str)

    #convert the combination dataframe into a ratings dataframe for predictions
    combo_ratings = pd.melt(combos_df, id_vars=['user_id'], value_vars=['book1', 'book2', 'book3'])
    combo_ratings['variable'] = 5
    combo_ratings.columns = ['user_id', 'rating', 'book_id']
    combo_ratings = combo_ratings[['user_id', 'book_id', 'rating']]
    return combo_ratings

def run_train_model():
    """Orchestrates getting the data from config file arguments."""

    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['train_model']

    combo_ratings = get_combo_df(**config_try['get_combo_df'])
    logger.info(combo_ratings.head())

if __name__ == "__main__":
    run_train_model()


