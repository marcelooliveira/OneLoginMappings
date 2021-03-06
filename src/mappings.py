# pip install pipenv
# pipenv install requests
from mysecrets import ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET

import requests
import json

# 1. Complete the following steps using the OneLogin API. Show a screenshot for each:
api_domain = 'https://api.us.onelogin.com'
r = requests.post(api_domain + '/auth/oauth2/v2/token',
  auth=(ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET),
  json={
    "grant_type": "client_credentials"
  }
)
response = r.json()

access_token = response['access_token']
headers = headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}

# 2. Create a role named “TorontoReader”. 

response = requests.get(api_domain + '/api/1/roles?name=TorontoReader', headers=headers)
json_data = json.loads(response.content)
toronto_reader_role_id = json_data['data'][0]['id']

# 3. Create a role named “MontrealReader”.

response = requests.get(api_domain + '/api/1/roles?name=MontrealReader', headers=headers)
json_data = json.loads(response.content)
montreal_reader_role_id = json_data['data'][0]['id']

# 4. Create two OneLogin apps called “TorontoNews” and “MontrealNews” using the OneLogin Access Template (connector type).

# 4.1. Get Connector Id for 'OneLogin Access Template'
response = requests.get(api_domain + '/api/2/connectors?name=OneLogin+Access+Template', headers=headers)
json_data = json.loads(response.content)
connector_id = json_data[0]['id']

# 4.2. Create apps with roles assigned to them
app_data = { "connector_id": connector_id, "name": "TorontoNews", "role_ids": [toronto_reader_role_id] }
response = requests.post(api_domain + '/api/2/apps', headers=headers, data=json.dumps(app_data))
json_data = json.loads(response.content)
toronto_app_id = json_data['id']

app_data = { "connector_id": connector_id, "name": "MontrealNews", "role_ids": [montreal_reader_role_id] }
response = requests.post(api_domain + '/api/2/apps', headers=headers, data=json.dumps(app_data))
json_data = json.loads(response.content)
montreal_app_id = json_data['id']

# 5. Complete the following steps using the OneLogin API. Show code samples demonstrating how to complete each step:

# 5.1. Using the API, create a mapping 
# that gives access to the MontrealNews app 
# to those users whose city = Montreal. Do
#  this by using “custom_attribute_city” as the condition source, 
# “=” as the condition operator, and “Montreal” as the condition value. 
# This mapping will have one action: “set_role”, with a value of “MontrealReader”.

mapping_data = {
   "name":"MontrealNews Mapping",
   "match":"all",
   "enabled":True,
   "position":None,
   "conditions":[
      {
         "source":"custom_attribute_city",
         "operator":"=",
         "value":"Montreal"
      }
   ],
   "actions":[
      {
         "action":"add_role",
         "value":[
            str(montreal_reader_role_id)
         ]
      }
   ]
}

response = requests.post(api_domain + '/api/2/mappings', headers=headers, data=json.dumps(mapping_data))
json_data = json.loads(response.content)
mapping_montreal_id = json_data['id']

# 5.2. Using the API, create a mapping 
# that gives access to the TorontoNews app 
# to those users whose city = Toronto.
# Do this by using “custom_attribute_city” as the condition source, 
# “=” as the condition operator, and “Toronto” as the condition value. 
# This mapping will have one action: “set_role”, with a value of “TorontoReader”.

mapping_data = {
   "name":"TorontoNews Mapping",
   "match":"all",
   "enabled":True,
   "position":None,
   "conditions":[
      {
         "source":"custom_attribute_city",
         "operator":"=",
         "value":"Toronto"
      }
   ],
   "actions":[
      {
         "action":"add_role",
         "value":[
            str(toronto_reader_role_id)
         ]
      }
   ]
}

response = requests.post(api_domain + '/api/2/mappings', headers=headers, data=json.dumps(mapping_data))
json_data = json.loads(response.content)
mapping_toronto_id = json_data['id']

# 5.3. Create a couple of users with city = Montreal and city = Toronto. 
# Notice that they are automatically assigned the MontrealReader or TorontoReader role,
# which grants them access to the application they need to use.

user_data = {
    "email": "amelie.gagnon@myemail.com",
    "firstname": "Amélie",
    "lastname": "Gagnon",
    "username": "Amélie Gagnon",
    "custom_attributes": {
      "city": "Montreal",
  }
}

response = requests.post(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))
json_data = json.loads(response.content)
user1_id = json_data['id']

user_data = {
    "email": "thomas.tremblay@myemail.com",
    "firstname": "Thomas",
    "lastname": "Tremblay",
    "username": "Thomas Tremblay",
    "custom_attributes": {
      "city": "Toronto",
  }
}

response = requests.post(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))
json_data = json.loads(response.content)
user2_id = json_data['id']

# 6. Give an example of how you’d use this in a business scenario:
# you could set up a mapping that automatically adds the “QuickbooksUser” role 
# to any new user whose department is “Accounting”.

# 7. Delete data
response = requests.delete(api_domain + '/api/2/mappings/' + str(mapping_montreal_id), headers=headers)
response = requests.delete(api_domain + '/api/2/mappings/' + str(mapping_toronto_id), headers=headers)

response = requests.delete(api_domain + '/api/2/users/' + str(user1_id), headers=headers)
response = requests.delete(api_domain + '/api/2/users/' + str(user2_id), headers=headers)

response = requests.delete(api_domain + '/api/2/apps/' + str(toronto_app_id), headers=headers)
response = requests.delete(api_domain + '/api/2/apps/' + str(montreal_app_id), headers=headers)

