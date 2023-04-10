import requests
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

params = {'$select': 'incident_datetime',
          '$limit': 2, 
          '$order': 'incident_datetime DESC',
          '$where': 'incident_datetime IS NOT NULL'}

r = requests.get(config.get('domain').get('url') + config.get('dataset').get('san_francisco_data') + '.json', 
                 params=params, 
                 headers=config.get('headers')
                )
if r.status_code != 200:
    raise RuntimeError('Can''t retrieve latest timestamp.' + r.text)

filename = os.path.abspath(os.curdir) + "\\files\\dataset_response.csv"
os.makedirs(os.path.dirname(filename), exist_ok=False)
with open(filename, 'w') as f:
    response= r.json()
    f.write(str(response))
