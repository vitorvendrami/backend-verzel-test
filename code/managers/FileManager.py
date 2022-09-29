from uuid import UUID, uuid4

import boto3

from app import app, S3_BUCKET

default_s3_bucket = S3_BUCKET

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"],
)


class FileManager:
    """Class to handle Files"""

    @staticmethod
    def generate_new_protected_file_name(extension):
        """Generates a hash to the name of the file"""

        file_name = uuid4().__str__()
        return file_name + extension

    @staticmethod
    def upload_file_to_s3(
        file, file_name, bucket_name=default_s3_bucket, acl="public-read"
    ):
        """
        Uploads a file for s3
        Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
        """

        try:
            s3.upload_fileobj(
                file,
                bucket_name,
                file_name,
                ExtraArgs={
                    "ContentType": file.content_type  # Set appropriate content type as per the file
                },
            )
        except Exception as e:
            print("Something Happened: ", e)
            return False, {"error": e}

        return True, "{}{}".format(app.config["S3_LOCATION"], file_name)

    @staticmethod
    def remove_file_from_s3(file_name: UUID, bucket_name=default_s3_bucket):
        """Removes a file from s3"""

        try:
            s3.delete_object(Bucket=bucket_name, Key=file_name)
        except Exception as e:
            return False, {"error", e}
        return True, {"Success": "Deleted Successfully"}

    @staticmethod
    def renew_file_from_s3(
        file,
        old_file_name: UUID,
        new_file_name: str,
        bucket_name: str = default_s3_bucket,
    ):
        """Delete an old file and uploads a new one"""

        deleted, uploaded, message = False, False, False

        try:
            deleted, message = FileManager.remove_file_from_s3(
                old_file_name, bucket_name
            )
            if deleted:
                uploaded, message = FileManager.upload_file_to_s3(
                    file, new_file_name, bucket_name
                )

        except Exception as e:
            return False, message

        return uploaded, message
