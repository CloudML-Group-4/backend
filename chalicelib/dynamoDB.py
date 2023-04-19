import boto3
from botocore.errorfactory import ClientError   # REF (Exception handling): stackoverflow.com/questions/33068055
from fuzzywuzzy import fuzz

class DB:
  def __init__(self, aws_access_key_id, aws_secret_access_key):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)   # REF (DB and Table): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    self.table = dynamodb.Table('datastore')
  
  def insert_item(self, item: dict):
    try:
      return self.table.put_item(Item=item)   # REF (Table .put_item): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/put_item.html
    except ClientError as e:
      return {'error': 'dynamoDB error while inserting an item: ' + e}

  def find_id(self, item_id:str):
    result = self.table.get_item(Key={'id': item_id})   # REF (Table .get_item): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
    return result['Item'] if 'Item' in result.keys() else {'warning': 'No such item in database.'}
  
  def find_item(self, name: str):
    response = self.table.scan()
    result = []
    for item in response['Items']:
      # TO DO: this needs work, an if statement before the append to check usernames close to the response
      # Might use "fuzzywuzzy, .token_sort_ratio": towardsdatascience.com/string-matching-with-fuzzywuzzy-e982c61f8a84
      # REF (FuzzyWuzzy string matching reference): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html   and   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html
      #### check if there are items (usernames) within the range?

      # TO DO: May have to play with this number a bit?
      if fuzz.token_set_ratio(name.lower(), item['username'].lower()) > 50:
        result.append(item)
    return result if result else {'warning':'No such item in database.'}
  
  def update_item(self, item: dict):
    try:
      # REF (): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html
      response = self.table.update_item(
        Key = {'id': item['id']},
        UpdateExpression = 'set username=:n, phone=:p, email=:e, address=:a',
        ExpressionAttributeValues = {
          ':n': item['name'] if 'name' in item.keys() else None,
          ':p': item['phone'] if 'phone' in item.keys() else None,
          ':e': item['email'] if 'email' in item.keys() else None,
          ':w': item['website'] if 'website' in item.keys() else None,
          ':a': item['address'] if 'address' in item.keys() else None
        },
        ReturnValues='UPDATED_NEW'
      )
      return response
    except ClientError as e:
      return {'error': 'dynamoDB error while updating an item: ' + e}
    