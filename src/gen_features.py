import pandas as pd
import numpy as np
import logging
import argparse
import yaml
from get_data import download_from_S3

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

def get_books_df(csv_dict):
    '''Reads in the csvs based on the names and files in the dictionary, 
      merges the books data with the tag id numbers, then merges the tag descriptions to the tag id numbers.
      Merges these into one dataframe
    
    Args:
        csv_dict (Dictionary): A dictionary with the key as what will be the name of the pandas dataframe, and a 
                               value as the location of the csv file to be read in
    Returns:
        book_tags_w_names (pandas.DataFrame): DataFrame containing books with the tag descriptions
    '''

    #read in csv files
    data_dict =  {}
    for key, value in csv_dict.items():
        data_dict[key] = pd.read_csv(value)    

    #merge book titles and ids to the book tags dataframe, then merge in tag names
    book_names = data_dict['books']
    book_names = book_names[['book_id', 'goodreads_book_id', 'title']]
    book_tags = data_dict['book_tags']
    tags_xwalk = data_dict['tags_xwalk']
    book_tags_w_names = pd.merge(book_tags, tags_xwalk, how='left', on=['tag_id'])
    book_tags_w_names = pd.merge(book_tags_w_names, book_names, how='left', on=['goodreads_book_id'])

    #Remove books with negative tags (Kindle Paperwhite User's Guide, and Kindle User's Guide)
    removing = book_tags_w_names[book_tags_w_names['count'] <=0]
    removing = removing[['title']]
    logger.warning("Books with negative tags removed!")
    logger.warning(removing)
    book_tags_w_names = book_tags_w_names[book_tags_w_names['count'] > 0]
    logger.info(book_tags_w_names.head())
    return book_tags_w_names

def get_genres(df, genre_dict):
    '''Creates a genre for each book based on the popular tag descriptions for that book
    
    Args: 
        df (pandas.DataFrame): the book_tags_w_names dataframe created by get_books_df
        genre_dict (dictionary): A dictionary with the name of the genre as the key, 
                                and tag descriptions describing this genre
    Returns:
        books_w_genres (pandas.DataFrame): A dataframe containing each book and its new genre
    '''
    
    #create genre column from book tags
    df['genre'] = np.nan
    for key, values in genre_dict.items():
        for value in values:
            df.loc[df['tag_name'] == value, 'genre'] = key
    
    #drop missing genres
    df = df[df.genre.notnull()]
    assert df['genre'].isna().sum() == 0

    #get top genre for each book
    df =df.groupby(['book_id','title','goodreads_book_id','genre'], as_index = False).sum()
    df = df.sort_values(['book_id', 'count'], ascending=[True, False])
    books_w_genres = df.groupby('book_id').first().reset_index()
    count = books_w_genres['genre'].value_counts().to_dict()
    logger.info("Number of Books in each Genre")
    logger.info(count)
    return books_w_genres

def drop_genre(df, genres_to_drop = []):
    '''Dropping any genres of the users choice -
       generally the genres the user decides do not have enough ratings or books
    
    Args:
        df (pandas.DataFrame): the books_w_genres dataframe created by get_genres
        genres_to_drop (list): the genres the user wishes to drop
    Returns:
        df (pandas.DataFrame): A dataframe without the genres the user dropped
    '''

    if genres_to_drop:
        for i in range(len(genres_to_drop)):
            genre = genres_to_drop[i]
            df = df[df['genre']!=genre]
    logger.info("Genres dropped:")
    logger.info(genres_to_drop)
    return df

def get_genre_rating_dfs(df, ratings_csv):
    """Merge the ratings file with the books with genres dataframe
 
    Args:
        df (pandas.DataFrame): the dataframe created by books_w_genres and drop_genre
        ratings_csv (file path): the file with the book ratings
    Returns:
        books_w_genres (pandas.DataFrame): the dataframe with books, the genre, and the ratings
                                           to be used by src/train_model.py
    """
    ratings = pd.read_csv(ratings_csv)

    books_w_genres = df[['book_id', 'goodreads_book_id', 'title', 'genre']]
    books_w_genres = books_w_genres.merge(ratings, how='left', on='book_id')
    logger.info(books_w_genres.head())
    return books_w_genres

def run_gen_features(args):
    """Orchestrates getting the data from config file arguments."""
    
    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_try = config['gen_features']

    bucket_name = args.input
    path = args.output

    download_from_S3(bucket_name, **config_try['download_from_S3'])
    book_tags_w_names = get_books_df(**config_try['get_books_df'])
    books_w_genres = get_genres(book_tags_w_names, **config_try['get_genres'])
    books_w_genres = drop_genre(books_w_genres, **config_try['drop_genre'])
    books_w_genres = get_genre_rating_dfs(books_w_genres, **config_try['get_genre_rating_dfs'])
    books_w_genres.to_csv(path)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict books for new users")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="michel-avc-project-private",
			help="s3 bucket with data")
    parser.add_argument("--output", "-o",  default="data/books_w_genres.csv",
                        help="Path to save dataframe to input into model")
    args = parser.parse_args()

    run_gen_features(args)

