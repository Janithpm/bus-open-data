import boto3
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

file_handler = logging.FileHandler('offload_script.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

s3_client = boto3.client('s3')

def offload_data_to_s3(local_file_path, bucket_name, s3_file_path):
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
        logger.info(f"Successfully offloaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
    except Exception as e:
        logger.error(f"Failed to offload data to S3: {e}")

def main():
    local_file_path = 'bus_data.db'
    bucket_name = 'open-bus-data-location-dumps'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    s3_file_path = f'data_{timestamp}.db'

    if os.path.exists(local_file_path):
        offload_data_to_s3(local_file_path, bucket_name, s3_file_path)
    else:
        logger.error(f"File {local_file_path} does not exist.")

main()
