import boto3
import uuid

AWS_ACCESS_KEY = "YOUR_KEY"
AWS_SECRET_KEY = "YOUR_SECRET"
BUCKET_NAME = "ai-speaking-coach"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)


def upload_video(file_path):

    key = f"videos/{uuid.uuid4()}.mp4"

    s3.upload_file(
        file_path,
        BUCKET_NAME,
        key,
        ExtraArgs={"ACL": "public-read"}
    )

    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"

    return url