import boto3
from botocore.errorfactory import ClientError  # REF (Exception handling): stackoverflow.com/questions/33068055
from fuzzywuzzy import fuzz

class DB:
  def __init__(self, aws_access_key_id, aws_secret_access_key):
    self.table_name = 'datastore'
    self.client = boto3.client('dynamodb')
    self.create_table()
    self.id = 1
    
    
  def create_table(self):
    try:
      self.client.create_table(
        TableName = self.table_name,
        KeySchema=[
          {
            'AttributeName': 'id',
            'KeyType': 'HASH'
          }
        ],
        AttributeDefinitions=[
          {
            'AttributeName': 'id',
            'AttributeType': 'S'
          }
        ],
        ProvisionedThroughput={
          'ReadCapacityUnits': 1,
          'WriteCapacityUnits': 1
        }
      )
    except ClientError as e:
      return


  def insert_item(self, item: dict):
    data = {
      'id': {'S': item['id']},
      'image-id': {'S': item['image-id']},
      'username': {'S': item['username'].lower()},
      'phone': {'S': item['phone'] or 'NULL'},
      'email': {'S': item['email'] or 'NULL'},
      'website': {'S': item['website'] or 'NULL'},
      'address': {'S': item['address'] or 'NULL'},
      'iam-user': {'S': item['iam-user']},
      'access-id': {'S': item['access-id']},
      'imgUrl': {'S': item['imgUrl']}
    }
    try:
      result = self.client.put_item(TableName=self.table_name, Item=data)
      self.id += 1
      return result   # REF (Table .put_item): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/put_item.html
    except ClientError as e:
      return {'error': 'dynamoDB error while inserting an item: ' + str(e)}


  def find_id(self, item_id:str):
    response = self.client.scan(
      TableName = self.table_name,
      FilterExpression = "id = :id",
      ExpressionAttributeValues = {":id": {"S": item_id}}
    )
    return response['Items'][0]
  
  
  def find_item(self, name: str):
    response = self.client.scan(
      TableName = self.table_name,
      FilterExpression = "username = :name",
      ExpressionAttributeValues = {":name": {"S": name}}
    )
    return response['Items']
  
  
  def update_item(self, id, item: dict):
    try:
      # REF (): https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html
      response = self.client.update_item(
        TableName = self.table_name,
        Key = {"id": {'S': id}},
        UpdateExpression = 'set username=:n, phone=:p, email=:e, address=:a, website=:w',
        ExpressionAttributeValues = {
          ':n': {'S': item['username']} if 'username' in item.keys() else None,
          ':p': {'S': item['phone']} if 'phone' in item.keys() else None,
          ':e': {'S': item['email']} if 'email' in item.keys() else None,
          ':w': {'S': item['website']} if 'website' in item.keys() else None,
          ':a': {'S': item['address']} if 'address' in item.keys() else None
        },
        ReturnValues='UPDATED_NEW'
      )
      return response
    except ClientError as e:
      print( {'error': 'dynamoDB error while updating an item: ' + str(e)})
    
  def delete_item(self, id):
    response = self.client.delete_item(
      TableName = self.table_name,
      Key= {'id': {'S': id}}
    )
    print(response)