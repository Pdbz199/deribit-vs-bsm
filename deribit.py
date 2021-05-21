import os
from dotenv import dotenv_values
config = dotenv_values(".env")
import openapi_client
from openapi_client.rest import ApiException
# import datatable as dt

# Setup configuration instance
conf = openapi_client.Configuration()
# Setup unauthenticated client
client = openapi_client.ApiClient(conf)
publicAPI = openapi_client.PublicApi(client)
# Authenticate with API credentials
response = publicAPI.public_auth_get('client_credentials', '', '', config['CLIENT_ID'], config['CLIENT_SECRET'], '', '', '')
access_token = response['result']['access_token']

conf_authed = openapi_client.Configuration()
conf_authed.access_token = access_token
# Use retrieved authentication token to setup private endpoint client
client_authed = openapi_client.ApiClient(conf_authed)
privateAPI = openapi_client.PrivateApi(client_authed)

# Make requests
# TODO: Collect deribit contract prices and the underlying prices
#! This can probably be done with public_ticker_get
# public_get_instruments_get gets list of currently active contracts for specified currency and for kind='option'/'futures'
# print(publicAPI.public_get_instruments_get(currency='BTC', kind='option'))
# res = publicAPI.public_ticker_get(instrument_name='BTC-28MAY21-38000-P')
# print(res['result'])