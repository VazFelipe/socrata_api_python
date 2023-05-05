import json
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Params:
    params: dict
    start_date: str 

    def __post_init__(self):
        start_date_converted = datetime.strptime(self.start_date, "%Y-%m-%d")
        for key, value in self.params.items():        
                if key.startswith("$where"):
                    params_updated = {key: value + " <= '" + (datetime(start_date_converted.year, start_date_converted.month, start_date_converted.day) + timedelta(days=0, hours=23, minutes=59, seconds=59, microseconds=999999)).isoformat() + "'"}
                    self.params.update(params_updated)  
        return self.params

@dataclass
class Socrata(Params):
    get_url: str 
    get_headers: dict

    def api_connection(self):
        response = requests.get(url=self.get_url, headers=self.get_headers, params=self.params)
        return response

if __name__ == '__main__':
    Socrata

