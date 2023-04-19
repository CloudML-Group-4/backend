import boto3
from botocore.errorfactory import ClientError   # REF (Exception handling): stackoverflow.com/questions/33068055
# Assuming roles: https://learnaws.org/2022/09/30/aws-boto3-assume-role/

class IAM:
  def __init__(self, aws_access_key_id, aws_secret_access_key):
    self.iam = boto3.client('iam', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

  def create_user(self, username: str):
    try:
      # REF (Boto3 .create_user): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_user.html
      # TO-DO: check list, if in list do something
      response = self.iam.create_user(Path='', UserName=username)
      return {
        'iam-user': response['User']['Username'],
        'access_id': response['User']['UserId']
      }
    except ClientError as e:
      return {'error': 'IAM_service error while creating an IAM user: ' + e}  
  def delete_user(self, username: str):
    try:
      # REF (Boto3 .delete_user): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/delete_user.html
      response = self.iam.delete_user(UserName=username)
      return response   # Should be JSONified... or do we need a response?
    except ClientError as e:
      return {'error': 'IAM_service error while deleting an IAM user: ' + e}
    