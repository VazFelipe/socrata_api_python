import json
from datetime import date

with open('config.json', 'r') as f:
    config = json.load(f)

get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
get_headers = config.get('api').get('headers')
# params = []

params = dict(config.get('api').get('params'))
start_date = date.today()

for key, value in params.items():
    if key.startswith("$where"):
        params_updated = {key: value + " <= " + str(start_date)}
        params.update(params_updated)
    print(key, value)

print(params)