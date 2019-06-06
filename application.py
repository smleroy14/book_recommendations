from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from src.create_db import Book_Recommendations
import pandas as pd
import traceback
import logging


# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("penny-lane")
logger.debug('Test log')

# Initialize the Flask application
app = Flask(__name__)
# Configure flask app from flask_config.py
app.config.from_pyfile('flask_config.py')

db = SQLAlchemy(app)

genre = ''


@app.route('/')
def intro_page():
   """Main view that lists genres in the database.
    Create view into index page that uses data queried from Book recs database and
    inserts it into the /templates/choose_genre.html template.
    Returns: rendered html template
    """
    
    logger.info('At introductory app page.')
    return render_template('choose_genre.html')

if __name__ == "__main__":
	
	app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
