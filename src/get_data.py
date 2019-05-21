
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import argparse

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)
logger = logging.getLogger(__file__)

#download raw Kaggle data from Public S3 bucket
s3 = boto3.client('s3')
s3.download_file('michel-avc-project', 'raw/books.csv', 'data/raw_from_s3/books.csv')
s3.download_file('michel-avc-project', 'raw/book_tags.csv', 'data/raw_from_s3/book_tags.csv')
s3.download_file('michel-avc-project', 'raw/ratings.csv', 'data/raw_from_s3/ratings.csv')
s3.download_file('michel-avc-project', 'raw/tags.csv', 'data/raw_from_s3/tags.csv')
s3.download_file('michel-avc-project', 'raw/to_read.csv', 'data/raw_from_s3/to_read.csv')

