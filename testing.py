import json
from datetime import datetime, date, timedelta
from utils import *

with open('config.json', 'r') as f:
    config = json.load(f)

get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
get_headers = config.get('api').get('headers')
# params = []

params = dict(config.get('api').get('params'))
start_date = date.today()

for key, value in params.items():
    if key.startswith("$where"):
        params_updated = {key: value + " <= '" + (datetime(start_date.year, start_date.month, start_date.day) + timedelta(days=0, hours=23, minutes=59, seconds=59, microseconds=999999)).isoformat() + "'"}
        params.update(params_updated)

# for key, value in params.items():
#     if key.endswith("date"):
#         args_dict_updated = {key: (value + timedelta(days=0, hours=23, minutes=59, seconds=59, microseconds=999999)).isoformat()}
#         params.update(args_dict_updated)

# new_params = Utils(params).modify_entry_params()
print(params["$where"])