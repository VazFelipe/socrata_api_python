import json
import requests
from dataclasses import dataclass

with open('config.json', 'r') as f:
    config = json.load(f)

get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
get_headers = config.get('api').get('headers')
params = config.get('api').get('params')

@dataclass
class Socrata:
    get_url: str
    get_headers: dict
    params: dict

    def api_connection(self):
        response = requests.get(self.get_url, headers=self.get_headers, params=self.params)
        return response

if __name__ == '__main__':
    Socrata()