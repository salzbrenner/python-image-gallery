import boto3
import logging
from botocore.exceptions import ClientError


def get_object(bucket_name, key):
    try:
        s3_client = boto3.client('s3')
        result = s3_client.get_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return None
    return result


def upload_file(file, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file.filename

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(
            file,
            bucket,
            object_name,
            ExtraArgs={'ACL': 'public-read', 'ContentType': file.mimetype})
        return True
    except ClientError as e:
        logging.error(e)
        return False


def delete_file(filename, bucket):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.delete_object(
            Bucket=bucket,
            Key=filename)
        return True
    except ClientError as e:
        logging.error(e)
        return False