import json
import requests
from datetime import timedelta
from dataclasses import dataclass, field

@dataclass
class Socrata:
    get_url: str 
    get_headers: dict
    start_date: str 

    def specify_params(self):
        for key, value in self.params.items():
                if key.startswith("$where"):
                    params_updated = {key: value + " <= " + self.start_date}
                    self.params.update(params_updated)  
        return self.params

    params: dict = field(default_factory=specify_params)
    
    def api_connection(self):
        response = requests.get(url=self.get_url, headers=self.get_headers, params=self.params)
        return response

if __name__ == '__main__':
    Socrata()