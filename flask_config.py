import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "book-rec"


#--------------
#RDS DATABASE
#--------------

#conn_type = "mysql+pymysql"
#user = os.environ.get("MYSQL_USER")
#password = os.environ.get("MYSQL_PASSWORD")
#host = os.environ.get("MYSQL_HOST")
#port = os.environ.get("MYSQL_PORT")
#DATABASE_NAME = 'msia423'
#SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
#SQLALCHEMY_TRACK_MODIFICATIONS = True
#HOST = "0.0.0.0"
#SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
#MAX_ROWS_SHOW = 100

#----------------------
#LOCAL SQLLITE DATABASE
#----------------------

SQLALCHEMY_DATABASE_URI = 'sqlite:///data/database.db?check_same_thread=False'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100


