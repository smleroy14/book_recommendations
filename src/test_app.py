import unittest
import pandas as pd
import numpy as np
import math
import collections

from gen_features import get_books_df, get_genres, drop_genre, get_genre_rating_dfs
from train_model import get_combo_df, train_model, get_top_n, take, get_recs
from score_model import precision_recall_at_k, get_accuracy


#Tests for src/gen_features.py


#def test_get_books_df():
#    """ Tests that get_books produces a dataframe with the correct columns"""

#    books_df = get_books_df( {'book_tags': 'data/raw_private_s3/book_tags.csv', 'tags_xwalk' : 'data/raw_private_s3/tags.csv', 'books' : 'data/raw_private_s3/books.csv'}) 
#    assert type(books_df) is pd.core.frame.DataFrame
#    column_names = list(books_df.columns.values)
#    assert column_names == ['goodreads_book_id', 'tag_id', 'count', 'tag_name', 'book_id', 'title'] 

def test_get_books_df_bad():
    """ Tests that get_books handles getting files that don't exist"""
    bad_dict =  {'book_tags': 'data/raw_private_s3/book_tags.csv', 'tags_xwalk' : 'data/raw_private_s3/tags.csv', 'books' : 'data/raw_private_s3/books_doesnt_exist.csv'}
    try:
        get_books_df(bad_dict)
    except FileNotFoundError:
        assert True

test_get_books_df_bad()    
#def test_get_genres():
#    """ Tests that each genre in the dictionary has books mapped to it"""
    
#    #calling get_books_df to get the proper dataframe for input
#    books_df = get_books_df( {'book_tags': 'data/raw_private_s3/book_tags.csv', 'tags_xwalk' : 'data/raw_private_s3/tags.csv', 'books' : 'data/raw_private_s3/books.csv'})
#    genre_dict = { 'Fiction' : ['fiction', 'adult-fiction', 'general-fiction'] , 'Fantasy' : ['fantasy', 'magic'], 'Young Adult': ['young-adult', 'ya', 'teen'], 'Classics' : ['classics', 'literature'], 'Romance': ['romance'], 'Mystery': ['mystery', 'thriller', 'crime', 'suspense'], 'Non-Fiction': ['non-fiction', 'nonfiction'], 'Biography': ['memoir', 'biography'], 'History': ['historical', 'history'], 'Historical Fiction' : ['historical-fiction'], 'Science Fiction': ['sci-fi', 'sci-fi-fantasy'], 'Childrens' : ['childrens', 'children-s', 'kids', 'children-s-books'], 'Graphic Novel': ['graphic-novels', 'comics', 'graphic-novel'], 'Adventure': ['adventure'], 'Dystopian': ['dystopian', 'dystopia'], 'Chick-lit': ['chick-lit'], 'Humor' : ['humor']}
    
#    genre_df = get_genres(books_df, genre_dict)
#    genre_list = genre_df['genre'].unique().tolist()
#    print(genre_list)    
#    assert len(genre_list)==17

#def test_drop_genre():
#    """ Testing that not dropping any genres works, and that dropping one genre leads to one less genre in the column """
#    #calling previous functions to get proper dataframe
#    books_df = get_books_df( {'book_tags': 'data/raw_private_s3/book_tags.csv', 'tags_xwalk' : 'data/raw_private_s3/tags.csv', 'books' : 'data/raw_private_s3/books.csv'})
#    genre_dict = { 'Fiction' : ['fiction', 'adult-fiction', 'general-fiction'] , 'Fantasy' : ['fantasy', 'magic'], 'Young Adult': ['young-adult', 'ya', 'teen'], 'Classics' : ['classics', 'literature'], 'Romance': ['romance'], 'Mystery': ['mystery', 'thriller', 'crime', 'suspense'], 'Non-Fiction': ['non-fiction', 'nonfiction'], 'Biography': ['memoir', 'biography'], 'History': ['historical', 'history'], 'Historical Fiction' : ['historical-fiction'], 'Science Fiction': ['sci-fi', 'sci-fi-fantasy'], 'Childrens' : ['childrens', 'children-s', 'kids', 'children-s-books'], 'Graphic Novel': ['graphic-novels', 'comics', 'graphic-novel'], 'Adventure': ['adventure'], 'Dystopian': ['dystopian', 'dystopia'], 'Chick-lit': ['chick-lit'], 'Humor' : ['humor']}

#    genre_df = get_genres(books_df, genre_dict)

#    dropped_df = drop_genre(genre_df, genres_to_drop = [])
#    assert genre_df.shape[0]==dropped_df.shape[0]
#    dropped_df2 = drop_genre(genre_df, genres_to_drop=['Fiction'])
#    full_list = genre_df['genre'].unique().tolist()
#    dropped_list = dropped_df2['genre'].unique().tolist()
#    assert len(full_list) == (len(dropped_list) + 1)

#def test_get_genre_rating_dfs():
#    """ Asserting that the function produces a dataframe with the correct columns and that rating is between 1 and 5"""
#    books_df = get_books_df( {'book_tags': 'data/raw_private_s3/book_tags.csv', 'tags_xwalk' : 'data/raw_private_s3/tags.csv', 'books' : 'data/raw_private_s3/books.csv'})
#    genre_dict = { 'Fiction' : ['fiction', 'adult-fiction', 'general-fiction'] , 'Fantasy' : ['fantasy', 'magic'], 'Young Adult': ['young-adult', 'ya', 'teen'], 'Classics' : ['classics', 'literature'], 'Romance': ['romance'], 'Mystery': ['mystery', 'thriller', 'crime', 'suspense'], 'Non-Fiction': ['non-fiction', 'nonfiction'], 'Biography': ['memoir', 'biography'], 'History': ['historical', 'history'], 'Historical Fiction' : ['historical-fiction'], 'Science Fiction': ['sci-fi', 'sci-fi-fantasy'], 'Childrens' : ['childrens', 'children-s', 'kids', 'children-s-books'], 'Graphic Novel': ['graphic-novels', 'comics', 'graphic-novel'], 'Adventure': ['adventure'], 'Dystopian': ['dystopian', 'dystopia'], 'Chick-lit': ['chick-lit'], 'Humor' : ['humor']}

#    genre_df = get_genres(books_df, genre_dict)
#    genre_rating_df = get_genre_rating_dfs(genre_df, "data/raw_private_s3/ratings.csv")
#    assert type(genre_rating_df) is pd.core.frame.DataFrame
#    column_names = list(genre_rating_df.columns.values)
#    print(column_names)
#    assert column_names == ['book_id', 'goodreads_book_id', 'title', 'genre', 'user_id', 'rating']
#    assert genre_rating_df['rating'].max()==5
#    assert genre_rating_df['rating'].min()==1

#Tests for src/train_model.py

#def test_get_combo_df():
#    """ Asserting that the number of combos is all of the combinations possible """
#    df = pd.read_csv("data/books_w_genres.csv")
#    combo_ratings, data, num_combos = get_combo_df(df, "History", 20, 3)
#    assert num_combos == (math.factorial(20)/(math.factorial(3)*math.factorial(20-3)))

#def test_train_model_df():
#    """ Asserting that the predictions returned from train_model is a list"""
#    df = pd.read_csv("data/books_w_genres.csv")
#    combo_ratings, data, num_combos = get_combo_df(df, "History", 20, 3)
#    predictions = train_model(combo_ratings, data, neighbors = 30, min_neighbors = 5, seed = 12345)
#    assert type(predictions) is list 

#def test_get_top_n():
#    """ asserting that the top_n returned from get_top_n is a dictionary"""
#    df = pd.read_csv("data/books_w_genres.csv")
#    combo_ratings, data, num_combos = get_combo_df(df, "History", 20, 3)
#    predictions = train_model(combo_ratings, data, neighbors = 30, min_neighbors = 5, seed = 12345)
#    top_n = get_top_n(predictions, n_start = 17, n_end = 22)
#    assert type(top_n) is collections.defaultdict

#def test_take():
#    """ Asserting that take takes the first n items from a list """
#    n = 5
#    iterable = [1,2,3,4,5,6,7,8,9,10]
#    check = take(n, iterable)
#    assert check==[1,2,3,4,5]

#def test_get_recs():
#    """ asserting that get_recs returns a dataframe of the length of the number of combos"""
#    df = pd.read_csv("data/books_w_genres.csv")
#    combo_ratings, data, num_combos = get_combo_df(df, "History", 20, 3)
#    predictions = train_model(combo_ratings, data, neighbors = 30, min_neighbors = 5, seed = 12345)
#    top_n = get_top_n(predictions, n_start = 17, n_end = 22)
#    recs = get_recs(top_n, 100)
#    assert recs.shape[0]==100

# Tests for src/score_model.py
#Note there is only a test for get_accuracy, as this is a wrapper for the precision_recall_at_k function

#def test_get_accuracy():
#    """ Asserting that precision and recall from the scored model are between 0 and 1 """
#    df = pd.read_csv("data/books_w_genres.csv")
#    genre = "History"
#    prec, rec = get_accuracy(df, genre, neighbors = 30, min_neighbors = 5, seed = 12345, kfolds = 5, k=5, threshold=4)
#    assert prec >=0
#    assert prec <=1
#    assert rec >=0
#    assert rec <=1
