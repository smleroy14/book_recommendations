import yaml
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import argparse

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

def download_from_S3(bucket_name, save_path, s3_file_names, local_file_names):
    """ Downloads raw data files from an S3 bucket

    Args:
        bucket_name (str): the name of the S3 bucket
        save_path (str): the directory to save the downloaded files in
        s3_file_names (list): the names of the files in the S3 bucket
        local_file_names (list): the names of the files saved locally
    Returns:
        local_file_names: the files will be saved to the specified local path
    """

    for i in range(len(local_file_names)):
        s3_file = s3_file_names[i]
        local_file = save_path + local_file_names[i]
        try:
            s3 = boto3.client('s3')
            s3.download_file(bucket_name, s3_file, local_file)
            logger.info("Data was downloaded from %s", bucket_name)
            logger.info("Data was saved to %s", save_path)
        except botocore.exceptions.NoCredentialsError as e:
            logger.error("Invalid S3 credentials")
            sys.exit(1)
   
def run_get_data(args):

    """Orchestrates getting the data from config file arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_try = config['get_data']

    bucket_name = args.input
    save_path = args.output

    #call all my functions in this script here
    download_from_S3(bucket_name, save_path, **config_try['download_from_S3'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict books for new users")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="michel-avc-project",
                        help="The S3 bucket with the data")
    parser.add_argument("--output", "-o",  default="data/raw_from_s3",
                        help="The file path to save the data")
    args = parser.parse_args()

    run_get_data(args)
    
