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
def write_to_S3(local_file_names, bucket_name, s3_file_names):

    """
    Upload Files to S3

    :param local_file_name: The path and name of the local file to be uploaded
    :param bucket_name: The S3 bucket where the file will be stored
    :param s3_file_name: The name for the file in the S3 bucket
    """
    for i in range(len(local_file_names)):
        local_file = local_file_names[i]
        s3_file = s3_file_names[i]
        try:
            s3 = boto3.resource('s3')
            s3.Object(bucket_name, s3_file).put(Body=open(local_file, 'rb'))
            logger.info(s3_file + "uploaded to S3 bucket")
        except botocore.exceptions.NoCredentialsError as e:
            logger.error("Invalid S3 credentials")
            sys.exit(1)

if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.load(f)
    config_try = config['load_data_s3']
    write_to_S3(**config_try['write_to_S3'])

