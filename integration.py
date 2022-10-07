from multiprocessing.connection import wait
from time import sleep
from pecan import response
import requests
import json
from authlib.jose import jwt

api = 'https://api.eloverblik.dk/customerapi/api'

def api_get(url: str, token: str) -> requests.Response:
  _header = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(token)
  }
  response = requests.get(url, headers=_header)
  while response == 429 or response == 503:
    print('GET Request failed, trying again in 1 minute.')
    sleep(60)
    response = requests.get(url, headers=_header)
  return response
def api_post(url: str, token: str, data: str) -> requests.Response:
  _header = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
    'Authorization': 'Bearer {}'.format(token)
  }
  response = requests.post(url, headers=_header, data=data)
  while response == 429 or response == 503:
    print('GET Request failed, trying again in 1 minute.')
    sleep(60)
    response = requests.get(url, headers=_header)
  return response
def refresh() -> str:
  # TODO: Replace try/catch before pushing to production
  try:
    with open('secrets.json', 'r') as read:
      obj = json.load(read)
    _token = obj['token']
  except(OSError, KeyError):
    print("An error occurred while reading the JWT token.\nMake sure secrets.json exists and contains 'token' with the associated value.")
    exit()
  response = api_get(api + '/token', _token)
  if response.status_code == 200:
    obj = response.json()
    api_token = obj['result']
  else:
    print('GET Request failed ({}):\n'.format(response))
    print(response.headers)
    exit()
  response = requests.get(api + '/meteringpoints/meteringpoint/getcharges')
  return api_token
def first_time_only(token: str) -> str:
  response = api_get(api + '/meteringpoints/meteringpoints', token)
  return response.json()

api_token = refresh()