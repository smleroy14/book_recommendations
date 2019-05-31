import random
import pandas as pd

from surprise import Dataset
from surprise import Reader
from surprise import SVD, KNNBasic, KNNWithMeans, KNNWithZScore
from surprise import accuracy
from surprise.model_selection import KFold

from collections import defaultdict
import itertools 
from itertools import islice

import logging
import yaml
import argparse


#Logging file 
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)


def get_combo_df(genre_pickle_file, num_choices, num_picks):
    """ Iterates through the top 20 books of a genre and
    gets all combinations of choosing 3 of these
    
    Returns a dataframe of "users" with 5 ratings for the 
    books they chose
    """

    data = pd.read_pickle(genre_pickle_file)
    data = data[['user_id','book_id','rating']]

    #get top books for choices
    top_books = data.groupby(['book_id']).count().reset_index()
    top_books = top_books[['book_id']]
    top_books = top_books.head(num_choices)
    
    #sort on book id, so combos are always in increasing order for user_id 
    top_books = top_books.sort_values('book_id', ascending = True).reset_index()
    top_books[['book_id']]

    #convert these to a list
    top_for_combo = []
    for i in range(len(top_books)):
         top_for_combo.append(top_books['book_id'][i])

    #iterate through the top list to get all possible combinations
    combos = itertools.combinations(top_for_combo, num_picks)
    combos = list(combos)
    combos_df = pd.DataFrame(combos, columns=['book1', 'book2', 'book3'])

    #set the combo of three top picks as user id
    combos_df['user_id']=combos_df['book1'].astype(str)+', '+combos_df['book2'].astype(str)+', '+combos_df['book3'].astype(str)
    num_combos = combos_df.shape[0]

    #convert the combination dataframe into a ratings dataframe for predictions
    combo_ratings = pd.melt(combos_df, id_vars=['user_id'], value_vars=['book1', 'book2', 'book3'])
    combo_ratings['variable'] = 5
    combo_ratings.columns = ['user_id', 'rating', 'book_id']
    combo_ratings = combo_ratings[['user_id', 'book_id', 'rating']]
    logger.info(combo_ratings.head())
    return combo_ratings, data, num_combos

def train_model(new_users, data, neighbors = 30, min_neighbors = 5, seed = 12345):
	
	#ensure a nice distribution of ratings
	ratings_counts = data['rating'].value_counts().to_dict()
	logger.info(ratings_counts)

	#combine actual ratings with all possible ratings users could input
	full_data = new_users.append(data)
	
	#use surprise Reader function to read in data in surprise format
	reader = Reader(rating_scale=(1, 5))
	data = Dataset.load_from_df(full_data[['user_id', 'book_id', 'rating']], reader)
	
	trainset = data.build_full_trainset()
	algo = KNNBasic(k=neighbors, min_k=min_neighbors, random_state=seed)
	algo.fit(trainset)
        
	# Save the trained model object
	#if save_tmo is not None:
        #	with open(save_tmo, "wb") as f:
        #        	pickle.dump(model, f)
        # 	logger.info("Trained model object saved to %s", save_tmo)

	# predict all the cells without values
	testset = trainset.build_anti_testset()
	predictions = algo.test(testset)
	return predictions

def get_top_n(predictions, n_start = 17, n_end = 22):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n_start(int): The index of the start of recommendation to output for each user. Default
            is 17, So we don't recommend the books that the user already had to pick from
        n_end(int): The last index of recommendation to output for each user. Default is 22
		(will return five recommendations)

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[n_start:n_end]

    return top_n

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def get_recs(top_n, num_combos, path_save_recs):
    n_items = take(num_combos, top_n.items())
    preds = []
    for uid, user_ratings in n_items:
        pred = uid, [iid for (iid, _) in user_ratings]
        preds.append(pred)
    preds_df = pd.DataFrame(preds, columns = ['user', 'recommendations'])
    recs = preds_df.recommendations.apply(pd.Series) \
        .merge(preds_df, right_index = True, left_index = True) \
        .drop(["recommendations"], axis = 1)
    recs.columns = ['book1', 'book2', 'book3', 'book4', 'book5', 'user'] 
    recs.to_csv(path_save_recs, index = False)

def run_train_model():
    """Orchestrates getting the data from config file arguments."""

    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['train_model']

    combo_ratings, data, num_combos = get_combo_df(**config_try['get_combo_df'])
    predictions = train_model(combo_ratings, data, **config_try['train_model'])
    top_n = get_top_n(predictions, **config_try['get_top_n'])
    get_recs(top_n, num_combos, **config_try['get_recs'])

    

if __name__ == "__main__":
    run_train_model()


