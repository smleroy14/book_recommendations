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

def get_accuracy(df, genre, neighbors = 30, min_neighbors = 5, seed = 12345, kfolds = 5):
        data = df[df['genre']==genre]
        data = data[['user_id','book_id','rating']]
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(data[['user_id', 'book_id', 'rating']], reader)
        algo_KNNbasic = KNNBasic(k = neighbors, min_k = min_neighbors, random_state = seed)

        kf = KFold(n_splits=kfolds,random_state=seed)
        prec_list = []
        recalls_list = []
        for trainset, testset in kf.split(data):
            algo_KNNbasic.fit(trainset)
            predictions = algo_KNNbasic.test(testset)
            precisions, recalls = precision_recall_at_k(predictions, k=5, threshold=4)

	    # Precision and recall can then be averaged over all users
            logger.info("Precision:")
            logger.info(sum(prec for prec in precisions.values()) / len(precisions))
            precision = (sum(prec for prec in precisions.values()) / len(precisions))
            logger.info("Recall")
            logger.info(sum(rec for rec in recalls.values()) / len(recalls))
            recall = (sum(rec for rec in recalls.values()) / len(recalls))
            prec_list.append(precision)
            recalls_list.append(recall)

        prec = (sum(prec_list) / len(prec_list))
        rec = (sum(recalls_list) / len(recalls_list))
 
        text_file = open(args.output, "a")
        text_file.write("Genre: %s\r\n" % genre)
        text_file.write("Precision: %s\r\n" % prec)
        text_file.write("Recall: %s\r\n" % rec)
        
def run_score_model(args):
    """Orchestrates getting the data from config file arguments."""

    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_try = config['score_model']
    
    genres = config_try['genres']

    if args.input is not None:
        df = pd.read_csv(args.input)
        logger.info("Features for input into model loaded from %s", args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input in order to score the model.")

    text_file = open(args.output, "w")
  
    for genre in genres:
        logger.info("calculating precision and recall for %s", genre)
        get_accuracy(df, genre, **config_try['get_accuracy'])
    text_file.close()   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score the models")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="data/books_w_genres.csv",
                        help="Path to input data for scoring")
    parser.add_argument("--output", "-o", default="data/model_accuracy.txt",
                        help="Path to save model accuracy")
    args = parser.parse_args()

    run_score_model(args)

