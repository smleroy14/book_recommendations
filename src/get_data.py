import yaml
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import argparse

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

def download_from_S3(bucket_name, s3_file_names, local_file_names):
    #download raw Kaggle data files from Public S3 bucket
    for i in range(len(local_file_names)):
        s3_file = s3_file_names[i]
        local_file = local_file_names[i]
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, s3_file, local_file)
   
def run_get_data():

    """Orchestrates getting the data from config file arguments."""
    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['get_data']

    #call all my functions in this script here
    download_from_S3(**config_try['download_from_S3'])

if __name__ == "__main__":
    run_get_data()
    
