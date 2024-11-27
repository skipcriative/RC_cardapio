import boto3
import os
from werkzeug.utils import secure_filename
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class S3Handler:
    def __init__(self):
        # Initialize the S3 client using environment variables
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')

    def upload_file(self, file, folder='products'):
        """
        Upload a file to the specified S3 bucket and return its public URL.
        :param file: File object to upload
        :param folder: Folder name in the bucket where the file will be stored
        :return: Public URL of the uploaded file
        """
        try:
            # Generate a secure filename and unique object name
            filename = secure_filename(file.filename)
            object_name = f"{folder}/{uuid.uuid4().hex}_{filename}"

            # Upload the file to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                object_name,
                ExtraArgs={'ACL': 'public-read'}
            )

            # Generate the public URL
            s3_url = f"https://{self.bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{object_name}"
            return s3_url
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to S3: {str(e)}")
