import requests
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Params:
    parameters: dict
    start_date: str

    def __post_init__(self):   

        for key, value in self.parameters.items():

                if key.startswith("$where"):

                    params_updated = {key: value + " BETWEEN '" + str(self.start_date) + "' AND '" + (datetime.strptime(str(self.start_date),"%Y-%m-%dT%H:%M:%S") + timedelta(days=0, hours=23,minutes=59,seconds=59)).strftime("%Y-%m-%dT%H:%M:%S") + "'"}

                    self.parameters.update(params_updated)  

        logger.info('From {cls} the attr: {attr}'.format(cls=type(self.parameters).__name__, attr=self.parameters), exc_info=True)
        
        return self.parameters

@dataclass
class Socrata(Params):
    url: str 
    headers: dict

    def api_connection(self):

        response = requests.get(url=self.url, headers=self.headers, params=self.parameters)

        logger.info('From {cls} the attr: {attr}'.format(cls=type(response).__name__, attr=response), exc_info=True)
        
        return response

if __name__ == '__main__':
    Socrata

