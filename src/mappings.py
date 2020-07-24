from mysecrets import ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET
import requests
import json
# 1. Complete the following steps using the OneLogin API. Show a screenshot for each:

# pip install pipenv
# pipenv install requests

r = requests.post('https://api.us.onelogin.com/auth/oauth2/v2/token',
  auth=(ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET),
  json={
    "grant_type": "client_credentials"
  }
)
response = r.json()

access_token = response['access_token']
api_domain = 'https://api.us.onelogin.com'
headers = headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}

# 2. Create two OneLogin apps called “TorontoNews” and “MontrealNews” using the OneLogin Access Template (connector type).

# 2.1. Get Connector Id for 'OneLogin Access Template'
response = requests.get(api_domain + '/api/2/connectors?name=OneLogin+Access+Template', headers=headers)
json_data = json.loads(response.content)
connector_id = json_data[0]['id']

# 2.2. Create apps
app_data = { "connector_id": connector_id, "name": "TorontoNews" }
response = requests.post(api_domain + '/api/2/apps', headers=headers, data=json.dumps(app_data))
json_data = json.loads(response.content)
toronto_app_id = json_data['id']

app_data = { "connector_id": connector_id, "name": "MontrealNews" }
response = requests.post(api_domain + '/api/2/apps', headers=headers, data=json.dumps(app_data))
json_data = json.loads(response.content)
montreal_app_id = json_data['id']

# 3. Create a role named “TorontoReader” and assign it to the “TorontoNews” application. 
# 4. Create a role named “MontrealReader” and assign it to the “MontrealNews” application.
# 5. Add a custom user field named “City” with a short name of “city”
# 6. Complete the following steps using the OneLogin API. Show code samples demonstrating how to complete each step:
# 6.1. Using the API, create a mapping that gives access to the MontrealNews app to those users whose city = Montreal. Do this by using “custom_attribute_city” as the condition source, “=” as the condition operator, and “Montreal” as the condition value. This mapping will have one action: “set_role”, with a value of “MontrealReader”.
# 6.2. Using the API, create a mapping that gives access to the TorontoNews app to those users whose city = Toronto. Do this by using “custom_attribute_city” as the condition source, “=” as the condition operator, and “Toronto” as the condition value. This mapping will have one action: “set_role”, with a value of “TorontoReader”.
# 6.3. Create a couple of users with city = Montreal;  and city = Toronto. Notice that they are automatically assigned the MontrealReader or TorontoReader role, which grants them access to the application they need to use.
# 6.4. Give an example of how you’d use this in a business scenario: you could set up a mapping that automatically adds the “QuickbooksUser” role to any new user whose department is “Accounting”.  


# Delete apps
response = requests.delete(api_domain + '/api/2/apps/' + str(toronto_app_id), headers=headers)
response = requests.delete(api_domain + '/api/2/apps/' + str(montreal_app_id), headers=headers)

