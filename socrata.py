import utils
import requests
from dataclasses import dataclass

@dataclass
class Params:
    parameters: dict
    start_date: str

    def __post_init__(self):   
        my_log = utils.Log().logging.getLogger(__name__)
        for key, value in self.parameters.items():
                my_log.debug("Params Socrata API: {0}".format(key, value))
                if key.startswith("$where"):
                    my_log.debug("Params Socrata API: {0}".format(key))
                    params_updated = {key: value + " <= '" + self.start_date + "'"}
                    my_log.debug("Params Socrata API: {0}".format(params_updated))
                    self.parameters.update(params_updated)  

        my_log.debug("Params Socrata API: {0}".format(self.parameters))

        return self.parameters

@dataclass
class Socrata(Params):
    url: str 
    headers: dict

    def api_connection(self):
        my_log = utils.Log().logging.getLogger(__name__)
        response = requests.get(url=self.url, headers=self.headers, params=self.parameters)
        my_log.debug("Connection Socrata API: {0}".format(self.url, self.headers, self.parameters))
        return response

if __name__ == '__main__':
    Socrata

