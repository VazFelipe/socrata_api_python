import json
import requests
from dataclasses import dataclass

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