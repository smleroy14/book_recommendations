# Book Recommendation App project repository
# For Mid-Project Review

Author: Michel LeRoy
QA: Alicia Burris


<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Getting the predictions](#1-getting-the-predictions)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
  * [2. Run the App on AWS](#2-run-the-app-on-aws)
  * [3. Run the App Locally](#3-run-the-app-locally)
- [Sources](#sources)


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
├── application.py                    <- runs the flask app
├── backlog.md                        <- markdown file to keep the backlog and icebox
|
├── config                            <- Directory for logging file and database configurations
|   dbconfig                          File for future users to edit with their RDS or SQLlite configurations
│   ├── logging/                      <- Configuration files for python loggers
|
├── config.yml                        <- yaml configuration file for training and scoring the model
│
├── data                              <- Folder that contains data used or generated.
|   ├── raw_from_s3                   <- default folder for downloading raw data from public S3 bucket
|   ├── raw_private_S3                <- default folder for downloading data from the private S3 bucket
|   ├── recs                          <- default folder for storing the predicted user recommendations
│
├── deliverables                      <- slide deck for midproject review - powerpoint
|
├── flask_config.py                   <- configuration file for the flask app
├── Makefile                          <- Makefile to run getting the predictions for the app
|
├── notebooks                         <- Folder that contains notebooks used for EDA and model training 
|
├── requirements.txt                  <- Python package dependencies 
|
├── src                               <- Source data for the project 
│   ├── create_db.py                  <- Script for creating either a sqllite database or an RDS daatabase
|   ├── gen_features.py               <- Script for generating the dataframe to be used by train_model.py
|   ├── get_data.py                   <- Script for downloading raw kaggle files from a public S3 bucket
|   ├── insert_db.py                  <- Script for adding data to either the sqllite db or the RDS db
|   ├── load_data_s3.py               <- Script for uploading raw data files to a user's own S3 bucket
|   ├── score_model.py                <- Script for getting the cross validated precision and recall for the model
|   ├── train_model.py                <- Script to train the model and get the predictions
|
|
├── static                            <- Files for the flask app
|    ├── background-pic.jpg           <- background image for the web app
|
├── templates                         <- html templates for the web pages
|   ├── choose_books.html             <- html template for the user to choose their favorite books
|   ├── choose_genre.html             <- htmml template for the user to choose a genre
|   ├── error-generic.html            <- html template for an unspecified error
|   ├── error-nobook.html             <- html template for error if a user does not choose a book
|   ├── error-nogenre.html            <- html template for error if a user does not choose a gen
|   ├── error-samebooks.html          <- html template for error if a user chooses two or more books that are the same
|   ├── recommendations1.html         <- html template that displays a user's first recommendation
|   ├── recommendations2.html         <- html template that displays a user's second recommendation
|   ├── recommendations3.html         <- html template that displays a user's third recommendation
|   ├── recommendations4.html         <- html template that displays a user's fourth recommendation
|   ├── recommendations5.html         <- html template that displays a user's fifth recommendation


```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

# Running the application 
## 1. Getting the predictions

The make file will set up a vitual environment with all the required packages for you. However, due to an issue with the surprise package, you will need to install numpy first separately. 

Documented here: https://github.com/NicolasHug/Surprise/issues/188

Please run this first:

```bash
pip install numpy
```

Next, open the Makefile and change the bucket name on lines 8 and 11. 'michel-avc-project-private' should be the name of your own S3 bucket. 
Note: you will need to have an AWS bucket along with a key

Next, make sure you have your aws configurations set up, so you can access the S3 bucket.

This means you should have an aws access key id and an aws access secret key in the ~/.aws/credentials file.

For more information, see this link: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

To get the predictions that will populate the database, run: 

```bash
make all
```

**Note: To change inputs, outputs, or the config file in use, please edit the Makefile arguments

## 2. Run the app on AWS
### Create an RDS database:

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

`python src/insert_db.py --config=config.yml --input=data/recs/all_recs.csv --table=Book_Recommendations`

`python src/insert_db.py --config=config.yml --input=data/books_w_genres.csv --table=Top_Books`

### To run the application:

Open flask_config.py and make sure the lines under RDS Database are not commented out, and the lines under LOCAL sqllite database are commented out.

Then run

`python application.py`

Open the IP address of your EC2 instance plus the port 3000, and you should be able to use the app!

An example site is http://18.219.185.115:3000 (replace the 18.219.185.115 with your own EC2 instance IP address)

## 3. Run the App Locally

### If you instead want a local database, create a sqllite database:
 
 ```bash
 python src/create_db.py --SQL_URI=sqlite:///data/database.db
 ```
 
To add data to the sqllite database, run: 

`python src/insert_db.py --config=config.yml --input=data/recs/all_recs.csv --table=Book_Recommendations --SQL_URI=sqlite:///data/database.db`

`python src/insert_db.py --config=config.yml --input=data/books_w_genres.csv --table=Top_Books --SQL_URI=sqlite:///data/database.db`

Open flask_config.py and make sure the lines under LOCAL sqllite database are not commented out, and comment out the RDS database lines.

You must add **?check_same_thread=False** to the end of the SQL_URI. For example, this should be SQL_URI=sqlite:///data/database.db?check_same_thread=False

### To run the application:

`python application.py`

You should be able to interact with the app at the website http://127.0.0.1:3000/


## Sources

Data Source: https://github.com/zygmuntz/goodbooks-10k

Learning to use the Surprise Package: https://surprise.readthedocs.io/en/stable/FAQ.html
