import json
import requests
from datetime import timedelta
from dataclasses import dataclass

@dataclass
class Socrata:
    get_url: str
    get_headers: dict
    params: dict
    args_dict: dict

    def api_connection(self):
        response = requests.get(self.get_url, headers=self.get_headers, params=self.params)
        return response
    
    def add_time_date_params(self):
        for key, value in self.args_dict.items():
            if key.endswith("date"):
                args_dict_updated = {key: (value + timedelta(days=0, hours=23, minutes=59, seconds=59, microseconds=999999)).isoformat()}
                self.args_dict.update(args_dict_updated)
        return self.args_dict

if __name__ == '__main__':
    Socrata