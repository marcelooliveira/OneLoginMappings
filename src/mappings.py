# 1. Complete the following steps using the OneLogin API. Show a screenshot for each:
# 2. Create two OneLogin applications called “TorontoNews” and “MontrealNews” using the OneLogin Access Template (TIPO DE CONECTOR).
# 3. Create a role named “TorontoReader” and assign it to the “TorontoNews” application. 
# 4. Create a role named “MontrealReader” and assign it to the “MontrealNews” application.
# 5. Add a custom user field named “City” with a short name of “city”
# 6. Complete the following steps using the OneLogin API. Show code samples demonstrating how to complete each step:
# 6.1. Using the API, create a mapping that gives access to the MontrealNews app to those users whose city = Montreal. Do this by using “custom_attribute_city” as the condition source, “=” as the condition operator, and “Montreal” as the condition value. This mapping will have one action: “set_role”, with a value of “MontrealReader”.
# 6.2. Using the API, create a mapping that gives access to the TorontoNews app to those users whose city = Toronto. Do this by using “custom_attribute_city” as the condition source, “=” as the condition operator, and “Toronto” as the condition value. This mapping will have one action: “set_role”, with a value of “TorontoReader”.
# 6.3. Create a couple of users with city = Montreal;  and city = Toronto. Notice that they are automatically assigned the MontrealReader or TorontoReader role, which grants them access to the application they need to use.
# 6.4. Give an example of how you’d use this in a business scenario: you could set up a mapping that automatically adds the “QuickbooksUser” role to any new user whose department is “Accounting”.  

