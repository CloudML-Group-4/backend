#####
# Import
# Dataset: https://web.cs.wpi.edu/~claypool/mmsys-dataset/2011/stanford/mvs_images/business_cards.html
#######
import json, base64
from chalice import Chalice
from chalicelib import comprehend_service, dynamoDB, iam, recognition_service, storage_service

#####
# Init
#######
app = Chalice(app_name='backend')
app.debug = True

# {"message": "Missing Authentication Token"}   -   REF (Pass AWS credentials to boto3 as params): https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
aws_access_key_id = 'AKIAX4AYSAAKILMAYI6N'
aws_secret_access_key = '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'
storage_bucket = 'datacen300864022.aws.ai'   # doesn't have .aws.ai for some reason: 'team4-business-cards-bucket', for now whatever use this or change to yours for testing

comprehend_service = comprehend_service.Comprehend(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
db = dynamoDB.DB(aws_access_key_id, aws_secret_access_key)
iam = iam.IAM(aws_access_key_id, aws_secret_access_key)
storage_service = storage_service.Storage(storage_bucket, aws_access_key_id, aws_secret_access_key)
#recognition_service = recognition_service(storage_service)   # Needs the storage service
recognition_service = recognition_service.RecognitionService(storage_service, aws_access_key_id, aws_secret_access_key)

#####
# REST Endpoint routes (Planned)
#######

# /images
# - process file upload, save file to storage
@app.route('/images', methods=['POST'], cors=True)
def upload_image():
  request_data = json.loads(app.current_request.raw_body)   # Bring in the raw request from Chalice
  file_name = request_data['filename']   # From request, get filename
  file_bytes = base64.b64decode(request_data['filebytes'])   # Get the actual file data
  image_storage = storage_service.upload_file(file_name, file_bytes)
  return image_storage

# /images/{image_id}/detect-text
# - image to text and extract information 
@app.route('/images/{image_id}/detect-text', methods=['GET','POST'], cors=True)
def detect_text(image_id):
  detect_card_text = recognition_service.detect_text(image_id)
  if isinstance(detect_card_text, dict):
    return detect_card_text
  response_pii = comprehend_service.detect_pii(detect_card_text)
  response_phi = comprehend_service.detect_phi(detect_card_text)
  
  # Please note in the return block here, capitalised are returned from comprehend services.
  # Also below we can experiment with which service returns the best comprehension, 
  # 'name': response_pii['NAME'] if 'NAME' in response_pii.keys() else None, can become 'name': response_phi['NAME'] if ['NAME'] in response_phi.keys() else None,
  # Note the change from response_pii to response_phi
  return {
     'name': response_pii['NAME'] if 'NAME' in response_pii.keys() else None,
     'phone': response_pii['PHONE'] if 'PHONE' in response_pii.keys() else None,
     'email': response_phi['EMAIL'] if 'EMAIL' in response_pii.keys() else None,
     'website': response_pii['URL'] if 'URL' in response_pii.keys() else None,
     'address': response_pii['ADDRESS'] if 'ADDRESS' in response_pii.keys() else None
  }

# /contacts/{image_id}/save-text
# - upload an item. Note: Expected input: {name: '', phone: '', email: '', website: '', address: ''}
@app.route('/contacts/{image_id}/save-text', methods=['POST'], cors=True)
def save_text(image_id):
  request_data = json.loads(app.current_request.raw_body.decode("utf-8"))   # Bring in the raw request from Chalice
  print(request_data['name'].replace(' ', '-'))
  response_iam = iam.create_user(request_data['name'].replace(' ', '-'))   # Take care of spaces. .create_user() provides the iam-user and access_id
  item = {
    'id': image_id,
    'username': request_data['name'],
    'phone': request_data['phone'],
    'email': request_data['email'],
    'website': request_data['website'],
    'address': request_data['address'],
    'iam-user': response_iam['iam-user'],
    'access-id': response_iam['access_id']
  }
  db.insert_item(item)
  return {'access_id': response_iam['access_id']}

# /contacts/find-text
# - find an item by name. Note: Expected input: {name: ''}
@app.route('/contacts/find-text', methods=['POST'], cors=True)
def find_text():
  request_data = json.loads(app.current_request.raw_body)   # Bring in the raw request from Chalice
  return db.find_item[request_data['name']]

# /contacts/{image_id}/{access_id}/update-text
# - update an item. Note: Expected input: {name: '', phone: '', email: '', website: '', address: ''}
# TODO: hmmmm POST or PUT? change as required please
@app.route('/contacts/{image_id}/{access_id}/update-text', methods=['PUT'], cors=True)
def update_text(image_id, access_id):
  request_data = json.loads(app.current_request.raw_body)   # Bring in the raw request from Chalice
  item = db.find_id(image_id)
  if 'warning' in item.keys():   # If we toss a warning from the service code
    return item
  if access_id == item['access_id']:   # Check access
    item = {
      'id': image_id,
      'name': request_data['name'],
      'phone': request_data['phone'],
      'email': request_data['email'],
      'website': request_data['website'],
      'address': request_data['address']
    }
    return db.update_item(item)
  else:
    return {'warning': 'Permission Denied.'}

# /contacts/{image_id}/{access_id}/delete-text
# - delete an item. TODO: DELETE or POST?
@app.route('/contacts/{image_id}/{access_id}/delete-text', methods=['DELETE'], cors=True)
def delete_text(image_id, access_id):
  item = db.find_id(image_id)
  if 'warning' in item.keys():   # There was a problem so just return the item
    return item
  if access_id == item['access_id']:   # Check access
    iam.delete_user(item['iam-user'])
    return db.delete_item(image_id)
  else:
    return {'warning': 'Permission Denied.'}

# Default route from Chalice
#@app.route('/')
#def index():
#    return {'hello': 'world'}
