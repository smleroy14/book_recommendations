
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import argparse

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)
logger = logging.getLogger(__file__)

# upload raw data to configurable S3 bucket
def write_to_S3(local_file_name, bucket_name, s3_file_name):

    """
    Upload Files to S3

    :param local_file_name: The path and name of the local file to be uploaded
    :param bucket_name: The S3 bucket where the file will be stored
    :param s3_file_name: The name for the file in the S3 bucket
    """
    try:
        s3 = boto3.resource('s3')
        s3.Object(bucket_name, s3_file_name).put(Body=open(local_file_name, 'rb'))
        logger.info(s3_file_name + "uploaded to S3 bucket")
    except botocore.exceptions.NoCredentialsError as e:
        logger.error("Invalid S3 credentials")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Upload Files to S3")
    parser.add_argument('--local_file', default=None, type=str, help = 'The path and name of the local file to be uploaded')
    parser.add_argument('--bucket', default=None, type=str, help='Name of bucket to land files in S3')
    parser.add_argument('--s3_file', default=None, type=str, help = 'The name for the file in the S3 bucket')
    args = parser.parse_args()
    write_to_S3(args.local_file, args.bucket, args.s3_file)

