import boto3
from botocore.errorfactory import ClientError   # REF (Exception handling): stackoverflow.com/questions/33068055

class Storage:
  def __init__(self, storage_bucket, aws_access_key_id, aws_secret_access_key):
    try:
      self.client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
      self.bucket_name = storage_bucket
    except ClientError as e:
      return {'error': 'storage_service error: ' + e}

  def get_storage_location(self):
    return self.bucket_name
  
  def upload_file(self, file_name, file_bytes):
    try:
      self.client.put_object(Bucket=self.bucket_name, Body=file_bytes, Key=file_name, ACL='public-read')
      return {'fileId': file_name, 'fileUrl': 'https://s3.amazonaws.com/' + self.bucket_name + '/' + file_name}   # Changed from file_id and file_url
    except ClientError as e:
      return {'error': 'storage_service error: ' + e}
  