# Book Recommendation App project repository
# For Mid-Project Review

Author: Michel LeRoy
QA: Alicia Burris


<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
  * [2. Source data from public S3 bucket](#2-source-from-S3)
  * [3. Create an RDS Database](#3-initialize-the-database)
  * [4. Create a sqllite database](#4-run-the-application)


<!-- tocstop -->

## Project Charter 

**Vision**: 

Have you ever been to the library and wasted hours perusing the shelves not knowing what book you wanted to read next? Or, more likely, come home with 13 books and read none of them? Have you ever bought a book, only to feel that you wasted your money? This book recommendation system will solve your problems! You will get personalized recommendations for your favorite genres of literature.

**Mission**: 

Using a historical dataset of six million ratings for 10,000 books, allow users to pick a genre of literature, pick their favorite books from a drop-down list in this genre, and get a personalized recommendation on what to read next. Alternatively, if a user would like to explore a brand new to her genre, she can request a list of the most popular books in that genre. Users will be able to store their recommendations in a “to-read list” and come back to the site and rate these books after they read them. 

**Success criteria**: 

Machine Learning Performance Metric:

The goal of this recommendation system is to have a high precision metric. The goal of increasing precision is to show only books that the user will actually enjoy, as the cost of showing false positives is high. When we test our recommendation system, the precision metric should be at least 80%, i.e. if we were to recommend 5 books to a user, at least 4 would be ones that she would enjoy.

User Performance Metric: 

This will be measured in two ways. First, when a user is given a recommendation, he or she will be able to add this recommendation to a list of books he or she would like to read, or “skip” the recommendation by saying she has already read the book, or is not interested in reading this book. Ideally, we would like users to not skip books. 
The second measurement of user performance will be user engagement. How often do users return to the site? Do they mark their recommendations as read? How did they rate the recommendation? Do they request new recommendations?

## Repo structure 

```
├── README.md                         <- You are here
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
|   dbconfig                          File for future users to edit with their RDS configurations
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│
├── deliverables                      <- slide deck for midproject review
|
├── notebooks                         <- Folder that contains notebooks used for EDA and model training that will be developed into scripts later
|
├── src                               <- Source data for the project 
│   ├── create_db.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
|   ├── get_data.py                   <- Script for downloading raw kaggle files from a public S3 bucket
|   ├── load_data_s3.py               <- Script for uploading raw data files to a user's own S3 bucket
|
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Running the application 
### 1. To get the predictions that will populate the database, run: 

```bash
make all
```

** Note: The user will need to have an AWS bucket along with a key

**Note: To change inputs, outputs, or the config file in use, please edit the Makefile

### 2. Create an RDS database:
Fill in the config/dbconfig file with the following: 

MYSQL_USER=""

MYSQL_PASSWORD=""

MYSQL_HOST=""

MYSQL_PORT=""

DATABASE_NAME=""

Next, source these configurations using

```bash
echo 'source config/dbconfig' >> ~/.bashrc
source ~/.bashrc
```

Note: You have been kicked off the virtual environment that was made using the Makefile after running the source command
 
You need to run 

```bash
source book-env/bin/activate
```

Finally, to create the RDS database with these configurations, run: 

`python src/create_db.py`

To add the data to this RDS database, run:
`python src/insert_db.py --config=config.yml --input=data/recs/all_recs.csv --table=Book_Recommendations'

`python src/insert_db.py --config=config.yml --input=data/books_w_genres.csv --table=Top_Books' 


### 3. If you instead want a local database, create a sqllite database:
 
 ```bash
 python src/create_db.py --SQL_URI=sqlite:///data/database.db
 ```
 
To add data to the sqllite database, run: 

`python src/insert_db.py --config=config.yml --input=data/recs/all_recs.csv --table=Book_Recommendations --SQL_URI=sqlite:///data/database.db'

`python src/insert_db.py --config=config.yml --input=data/books_w_genres.csv --table=Top_Books --SQL_URI=sqlite:///data/database.db'


