import json
import requests
from dataclasses import dataclass

with open('config.json', 'r') as f:
    config = json.load(f)

get_url = config.get('api').get('domain').get('url')
get_headers = config.get('api').get('headers')
params_where_clause = config.get('api').get('params')

@dataclass
class Socrata:
    get_url: str
    get_headers =  dict
    params_where_clause = str
    params_limit_clause = int

    def api_connection(self, get_url, get_headers, params_where_clause, params_limit_clause):
        self.get_url = get_url
        self.get_headers = get_headers
        self.params_where_clause = params_where_clause
        self.params_limit_clause = params_limit_clause

        response = requests.get(self.get_url, self.get_headers, self.params_where_clause, self.params_limit_clause)

        return response

print(__name__)
if __name__ == '__main__':
    # print(type(config.get('api').get('headers')), config.get('api').get('headers'))
    print(params_where_clause)