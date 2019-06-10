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


def get_combo_df(df, genre, num_choices, num_picks):
    """ Iterates through the top 20 books of a genre and
    gets all combinations of choosing 3 of these. Creates 'ratings' by treating each book chosen 
   as a rating of 5, and each 'user_id' will be a string of the book ids they chose.

    Args:
        df (pandas.Dataframe): A dataframe of the books, genres, and ratings
        genre (str): The genre for which you want the top books
        num_choices (int): The number of top books a user will choose from
        num_picks (int): The number of books a user will pick from the top books
    Returns:
        combo_ratings (pandas.Dataframe): A dataframe with the book choices for all the possible combinations a user could input on the app
        data (pandas.Dataframe): A dataframe with all the actual ratings and books for a genre for the model
        num_combos (int): the number of possible new combinations based on num_choices and num_picks 
    """

    data = df[df['genre']==genre]
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
    """ Trains the KNN Basic model using the surprise package using
    the existing ratings data combined with all the new user possible combinations

    Args:
        new_users (pandas.Dataframe): The dataframe with the 'ratings' of all the possible combinations of user input
        data (pandas.Dataframe): The existing ratings dataframe 
        neighbors (int): the number of nearest neighbors to train the model on, default is 30
        min_neighbors (int): the minimum number of neighbors a user must have to receive a prediction. 
                            If there are not enough neighbors, the prediction is set the the global mean of all ratings
                            default is 5.
        seed (int): setting the random state, default is 122345
    Returns:
        predictions (list of prediction objects):  The predicted recommendations from the model
    """
	
    #ensure a nice distribution of ratings
    ratings_counts = data['rating'].value_counts().to_dict()
    logger.info("Ratings Distributions:")
    logger.info(ratings_counts)

    #combine actual ratings with all possible ratings users could input
    full_data = new_users.append(data)
	
    #use surprise Reader function to read in data in surprise format
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(full_data[['user_id', 'book_id', 'rating']], reader)
	
    trainset = data.build_full_trainset()
    algo = KNNBasic(k=neighbors, min_k=min_neighbors, random_state=seed)
    algo.fit(trainset)
        
    # predict all the cells without values
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    return predictions

def get_top_n(predictions, n_start = 17, n_end = 22):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n_start(int): The index of the start of recommendation to output for each user. Default
            is 17, So we don't recommend the books that the user already had to pick from
        n_end(int): The last index of recommendation to output for each user. Default is 22
		(will return five recommendations)

    Returns:
        top_n (dictionary): A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[n_start:n_end]
    logger.info("Retrieving top predictions for each user")
    return top_n

def take(n, iterable):
    """Helper function to return first n items of the iterable as a list"""
    return list(islice(iterable, n))

def get_recs(top_n, num_combos):
    """ Iterates through the dictionary of predictions and saves a 
    dataframe of recommendations for all the possible user inputs

    Args:
        top_n (dictionary): A dictionary where keys are user (raw) ids and values are lists of tuples:
                           [(raw item id, rating estimation), ...] of size n.
        num_combos (int): The number of possible user combinations
    Returns:
        recs (pandas.Dataframe): A dataframe with 5 recommendations for each possible new user
    """

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
    logger.info("Predictions retrieved")
    return recs

def run_train_model(args):
    """Orchestrates training the model from config file arguments."""

    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_try = config['train_model']

    path = args.output

    genres = config_try['genres']
    logger.info(genres)
    
    if args.input is not None:
        df = pd.read_csv(args.input)
        logger.info("Features for input into model loaded from %s", args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input for training.")

    all_recs = pd.DataFrame()
    for genre in genres:
        logger.info("getting predictions for %s", genre)
        combo_ratings, data, num_combos = get_combo_df(df, genre, **config_try['get_combo_df'])
        predictions = train_model(combo_ratings, data, **config_try['train_model'])
        top_n = get_top_n(predictions, **config_try['get_top_n'])
        recs = get_recs(top_n, num_combos)
        recs['genre'] = genre
        all_recs = all_recs.append(recs, ignore_index = True)
    all_recs.to_csv(path)
    logger.info("Recommendations saved to %s", path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict books for new users")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="data/books_w_genres.csv",
                        help="Path to input data for scoring")
    parser.add_argument("--output", "-o",  default="data/recs/all_recs.csv",
                        help="Path to where to save output predictions")
    args = parser.parse_args()

    run_train_model(args)


