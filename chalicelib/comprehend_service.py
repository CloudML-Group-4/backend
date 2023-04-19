import boto3
from botocore.errorfactory import ClientError   # REF (Exception handling): stackoverflow.com/questions/33068055

class Comprehend:
  def __init__(self, aws_access_key_id, aws_secret_access_key):
    self.comprehend = boto3.client('comprehend', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    self.comprehendmedical = boto3.client('comprehendmedical', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
  
  # detect_pii is detect personally identifiable information
  def detect_pii(self, text_line):
    try:
      # REF (detect_pii_entities to figure out what is an email or name, etc.): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/client/detect_pii_entities.html
      text = str()
      for line in text_line:
        text += line['text'] + '\n'
      response = self.comprehend.detect_pii_entities(Text=text, LanguageCode='en')
      result = {}
      for entity in response['Entities']:
        result[entity['Type']] = text[entity['BeginOffset']:entity['EndOffset']]
      return result
    except ClientError as e:
      return {'error': 'Comprehend error while while running detect_pii_entities: ' + str(e)}  
  
  # detect_phi is the health version of detect_pii, same idea, maybe a little better or worse
  def detect_phi(self, text_line):
    try:
      text = str()
      for line in text_line:
        text += line['text'] + '\n'
      response = self.comprehendmedical.detect_phi(Text=text)#, LanguageCode='en')
      result = {}
      for entity in response['Entities']:
        result[entity['Type']] = text[entity['BeginOffset']:entity['EndOffset']]
      return result
    except ClientError as e:
      return {'error': 'Comprehend Medical error while while running detect_phi: ' + str(e)}  
  