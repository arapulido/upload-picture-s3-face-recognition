import boto3
import os
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler(os.environ['APP_LOGS'] + 'face_recognition.log', maxBytes=10000, backupCount=1)
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '- %(message)s')
file_handler.setFormatter(Formatter(FORMAT))
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

def upload_file_to_s3(file, bucket_name, aws_access_key_id, aws_secret_access_key, acl="public-read"):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        logger.error("Error uploading to S3: %s", e)
        return False

    logger.info("Uploaded %s file to %s bucket", file.filename, bucket_name)
    return True
