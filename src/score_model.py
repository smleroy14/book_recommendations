import random
import pandas as pd

from surprise import Dataset
from surprise import Reader
from surprise import SVD, KNNBasic, KNNWithMeans, KNNWithZScore
from surprise import accuracy
from surprise.model_selection import KFold

from collections import defaultdict
import itertools

import logging
import yaml
import argparse


#Logging file
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

def precision_recall_at_k(predictions, k=10, threshold=3):
    '''Return precision and recall at k metrics for each user.'''

    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():

        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1

        # Recall@K: Proportion of relevant items that are recommended
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1

    return precisions, recalls

def get_accuracy(genre_pickle, neighbors = 30, min_neighbors = 5, seed = 12345, kfolds = 5):
	data = pd.read_pickle(genre_pickle)
	data = data[['user_id','book_id','rating']]
	reader = Reader(rating_scale=(1, 5))
	data = Dataset.load_from_df(data[['user_id', 'book_id', 'rating']], reader)
	algo_KNNbasic = KNNBasic(k = neighbors, min_k = min_neighbors, random_state = seed)

	kf = KFold(n_splits=kfolds)
	for trainset, testset in kf.split(data):
	    algo_KNNbasic.fit(trainset)
	    predictions = algo_KNNbasic.test(testset)
	    precisions, recalls = precision_recall_at_k(predictions, k=5, threshold=4)

	    # Precision and recall can then be averaged over all users
	    logger.info("Precision:")
	    logger.info(sum(prec for prec in precisions.values()) / len(precisions))
	    logger.info("Accuracy")
	    logger.info(sum(rec for rec in recalls.values()) / len(recalls))

def run_score_model():
    """Orchestrates getting the data from config file arguments."""

    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['score_model']

    get_accuracy(**config_try['get_accuracy'])

if __name__ == "__main__":
    run_score_model()

