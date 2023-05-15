import requests
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Params:
    parameters: dict
    start_date: str

    def __post_init__(self):   

        for key, value in self.parameters.items():

                if key.startswith("$where"):

                    params_updated = {key: value + " <= '" + self.start_date + "'"}

                    self.parameters.update(params_updated)  

        logger.info('From __post_init__ the parameters: {}'.format(self.parameters), exc_info=True)
        
        return self.parameters

@dataclass
class Socrata(Params):
    url: str 
    headers: dict

    def api_connection(self):

        response = requests.get(url=self.url, headers=self.headers, params=self.parameters)

        logger.info('From api_connection() the response: {}'.format(response), exc_info=True)
        
        return response

if __name__ == '__main__':
    Socrata

