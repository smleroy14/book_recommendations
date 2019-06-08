from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from src.create_db import Book_Recommendations, Top_Books
import pandas as pd
import traceback
import logging


# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('flask_config.py')

#Logging file 
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

#Initialize the database
db = SQLAlchemy(app)

genre = ''

@app.route('/')
def intro_page():
    """Main view that lists genres for the user to choose from.
    Returns: rendered html template
    """

    logger.info('At first page: choose_genre')
    logger.debug("Listing genres")
    return render_template('choose_genre.html')


@app.route('/choose_books', methods=['POST'])
def add_genre():
    """View that process a POST with the genre input and displays the top books for this genre, queried from DB.
    Returns: rendered html template
    """
    global genre
    genre = request.form['genre']
    try:
        top_books = db.session.query(Top_Books).filter_by(genre=genre)
        logger.info("Top books for %s accessed", genre)
        print(top_books)
        return render_template('choose_books.html', genre=genre, top_books=top_books)
    except:
        traceback.print_exc()
        logger.warning("User did not choose a book, error page returned")
        return render_template('error-nogenre.html')

@app.route('/recommendations', methods=['POST'])
def get_recs():
    """View that process a POST with book choice inputs and displays recommendations, queried from DB.
    Returns: rendered html template
    """
    try:
        firstbook = int(request.form['bookchoice1'])
        print(firstbook)
        secondbook = int(request.form['bookchoice2'])
        print(secondbook)
        thirdbook = int(request.form['bookchoice3'])
        print(thirdbook)
    except:
        traceback.print_exc()
        logger.warning("User did not pick a book, error no book page returned")
        return render_template('error-nobook.html')
    if firstbook==secondbook:
        return render_template('error-samebooks.html')
    if secondbook==thirdbook:
        return render_template('error-samebooks.html')
    if firstbook==thirdbook:
        return render_template('error-samebooks.html')
    user_id = str(firstbook) + ', ' + str(secondbook) + ', ' + str(thirdbook)
    print(user_id)
    try:
        recs = db.session.query(Book_Recommendations).filter_by(user=user_id)
        logger.debug("Recommendation Query Accessed for user %s", user_id)
        return render_template('recommendations.html', rec = recs)
    except:
        traceback.print_exc()
        logger.warning("Not able to display recommendations, error page returned")
        return render_template('error-generic.html')

if __name__ == "__main__":
    	
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
