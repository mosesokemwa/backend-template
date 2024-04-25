"""Download credentials files from AWS S3 based on environment."""


import os

import boto3
from decouple import config


def main():
    """Download credentials files based on the specified environment."""
    with open('build_env.txt', 'r') as file:
        env = file.readline().strip().upper()

    if env == 'PROD':
        bucket_name = 'fake-prod'
        key_docsupdator = 'fake.json'
        key_invest_platform = 'fake.json'
    else:
        bucket_name = 'backend-template-auth-files'
        key_docsupdator = 'docsupdator-88528ec20c6b.json'
        key_invest_platform = 'invest-platform-firebase-adminsdk-jyl9e-0d9b94e000.json'

    destination_folder = '/backend-template'

    download_file_from_s3(bucket_name, key_docsupdator, destination_folder)
    download_file_from_s3(bucket_name, key_invest_platform, destination_folder)


def download_file_from_s3(bucket_name, key, destination_folder):
    """
    Download a file from an S3 bucket to a local destination folder.

    Args:
        bucket_name (str): The name of the S3 bucket.
        key (str): The key of the file in the S3 bucket.
        destination_folder (str): The local destination folder to save the file.
    """
    s3 = boto3.client('s3',
                      aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

    # Download file from S3
    destination_path = os.path.join(destination_folder, os.path.basename(key))
    s3.download_file(bucket_name, key, destination_path)

    print(f"File downloaded to: {destination_path}")


if __name__ == "__main__":
    main()
