import boto3
from botocore.errorfactory import ClientError   # REF (Exception handling): stackoverflow.com/questions/33068055

class RecognitionService:
  def __init__(self, storage_service, aws_access_key_id, aws_secret_access_key):
    self.client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    self.bucket_name = storage_service.get_storage_location()

  def detect_text(self, file_name):
    # REF (rekog .detect_text): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_text.html
    try:
      response = self.client.detect_text(
        Image = {
            'S3Object': {
              'Bucket': self.bucket_name,
              'Name': file_name
          }
        }
      )
    except ClientError as e:
      return {'error': 'recognition_service error: ' + e}

    lines = []
    for detection in response['TextDetections']:
      if detection['Type'] == 'LINE':
        lines.append({
          'text': detection['DetectedText'],
          'confidence': detection['Confidence'],
          #'boundingBox': detection['Geometry']['BoundingBox']   # I don't think needed
        })
    return lines
