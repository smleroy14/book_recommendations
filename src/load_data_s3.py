import yaml
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import argparse

# set up logging config
logging.basicConfig(filename='config/logging.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

# upload raw data to configurable S3 bucket
def write_to_S3(bucket_name, file_path, local_file_names, s3_file_names):

    """
    Upload Files to S3

    Args: 
    bucket_name (str): The S3 bucket where the file will be stored
    file_path (str): the local file folder where the data is located   
    local_file_names (list): The names of the local files to be uploaded
    s3_file_names (list): The names for the files in the S3 bucket

    Returns:
       None - the files will be saved to the s3 bucket
    """
    for i in range(len(local_file_names)):
        local_file = file_path + local_file_names[i]
        s3_file = s3_file_names[i]
        try:
            s3 = boto3.resource('s3')
            s3.Object(bucket_name, s3_file).put(Body=open(local_file, 'rb'))
            logger.info("uploaded to S3 bucket %s", bucket_name)
        except botocore.exceptions.NoCredentialsError as e:
            logger.error("Invalid S3 credentials")
            sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Predict books for new users")
    parser.add_argument("--config", "-c", default="config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="michel-avc-project",
                        help="The S3 bucket with the data")
    parser.add_argument("--output", "-o",  default="data/raw_from_s3",
                        help="The file path to save the data")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_try = config['load_data_s3']

    file_path = args.input
    bucket_name = args.output

    write_to_S3(bucket_name, file_path, **config_try['write_to_S3'])

