import json
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class Params:
    parameters: dict
    start_date: str

    def __post_init__(self):   
        for key, value in self.parameters.items():        
                if key.startswith("$where"):
                    params_updated = {key: value + " <= '" + self.start_date + "'"}
                    self.parameters.update(params_updated)  
        return self.parameters

@dataclass
class Socrata(Params):
    url: str 
    headers: dict

    def api_connection(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.parameters)
        return response

if __name__ == '__main__':
    Socrata

