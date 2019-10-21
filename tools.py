import boto3
import logging

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
        logging.error("Error uploading to S3: ", e)
        return False

    logging.info("Uploaded %s file to %s bucket", file.filename, bucket_name)
    return True
