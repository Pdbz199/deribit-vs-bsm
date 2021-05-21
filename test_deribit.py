import os
from dotenv import dotenv_values
config = dotenv_values(".env")
import openapi_client

# Setup configuration instance
conf = openapi_client.Configuration()
# Setup unauthenticated client
client = openapi_client.ApiClient(conf)
publicApi = openapi_client.PublicApi(client)
# Authenticate with API credentials
# response = publicApi.public_auth_get('client_credentials', '', '', 'API_ACCESS_KEY', 'API_SECRET_KEY', '', '', '', scope='session:test wallet:read')
response = publicApi.public_auth_get('client_credentials', '', '', config['CLIENT_ID'], config['CLIENT_SECRET'], '', '', '')
access_token = response['result']['access_token']

conf_authed = openapi_client.Configuration()
conf_authed.access_token = access_token
# Use retrieved authentication token to setup private endpoint client
client_authed = openapi_client.ApiClient(conf_authed)
privateApi = openapi_client.PrivateApi(client_authed)

# Make requests
response = privateApi.private_get_transfers_get(currency='BTC')
print(response)
# print(response['result']['data'][0]['amount'])
response = privateApi.private_get_current_deposit_address_get(currency='BTC')
print(response)
# print(response['result']['address'])

# Unavailable functions:
# funding_rate_history