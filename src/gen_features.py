import pandas as pd
import logging
import argparse
import yaml
from get_data import download_from_S3

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

def get_books_df(csv_dict):
    '''Reads in the csvs based on the names and files in the dictionary, and merges these into one dataframe'''

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
    book_tags_w_names = book_tags_w_names[book_tags_w_names['count'] > 0]
    return book_tags_w_names

def get_genres(df, genre_dict):
    '''Creates a genre for each book based on the tags file'''
    
    #create genre column from book tags
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
    logger.info(count)
    return books_w_genres

def drop_genre(df, genres_to_drop = []):
    '''Dropping any genres without enough ratings or books'''
    if genres_to_drop:
        for i in range(len(genres_to_drop)):
            genre = genres_to_drop[i]
            df = df[df['genre']!=genre]
    return df

def get_genre_rating_dfs(df, ratings_csv):
    """Create a dictionary with a dataframe for each individual genre, and pickle each dataframe"""
    ratings = pd.read_csv(ratings_csv)
    print(ratings.head())

    books_w_genres = df[['book_id', 'goodreads_book_id', 'title', 'genre']]
    books_w_genres = books_w_genres.merge(ratings, how='left', on='book_id')
    return books_w_genres

def run_gen_features():
    """Orchestrates getting the data from config file arguments."""
    
    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_try = config['gen_features']

    path = args.output

    download_from_S3(**config_try['download_from_S3'])
    book_tags_w_names = get_books_df(**config_try['get_books_df'])
    books_w_genres = get_genres(book_tags_w_names, **config_try['get_genres'])
    books_w_genres = drop_genre(books_w_genres, **config_try['drop_genre'])
    books_w_genres = get_genre_rating_dfs(books_w_genres, **config_try['get_genre_rating_dfs'])
    books_w_genres.to_csv(path)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict books for new users")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--output", "-o",  default="data/books_w_genres.csv",
                        help="Path to save dataframe to input into model")
    args = parser.parse_args()

    run_gen_features(args)

