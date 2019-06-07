from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from src.create_db import Book_Recommendations
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


@app.route('/')
def intro_page():
    """Main view that lists genres for the user to choose from.
    Returns: rendered html template
    """

    logger.info('At first page: choose_genre')
    logger.debug("Listing genres")
    return render_template('choose_genre.html')
    

if __name__ == "__main__":
    	
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
