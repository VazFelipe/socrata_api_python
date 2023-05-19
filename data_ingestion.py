import json
import argparse
import logging.config
import time
from sys import argv
from datetime import date, datetime
from dataclasses import dataclass, field
from collections import defaultdict
from socrata import *
from utils import *
from storage import *

logger = logging.getLogger(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

parser = argparse.ArgumentParser(description="Extract the dataset named Police Department Incident Reports: 2018 to Present \
                                 from The City and Condado of San Francisco. Socrata Open Data API have been used to programmatically \
                                 return the dataset.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
type_modes = ["LAST_DATE", "REFRESH"]
parser.add_argument("-m", "--mode", type=str, choices=type_modes, default=type_modes[0], required=True, help="the reference is the last date")
parser.add_argument("-s", "--start_date", type=datetime.fromisoformat, default="2018-01-01", required=("--mode="+type_modes[1] in argv), help="used with refresh mode: from the desired date since 2018-01-01")
parser.add_argument("-e", "--end_date", type=datetime.fromisoformat, default=date.today(), required=("--mode="+type_modes[1] in argv), help="used with refresh mode: from the desired date since 2018-01-01")
args = vars(parser.parse_args())

@dataclass
class Data:
     start_date: str = field(init=False)
     end_date: str = field(init=False)
     get_url: str = field(init=False)
     get_headers: str = field(init=False)
     params: str = field(init=False)
     args_converted: "defaultdict[dict]" = field(default_factory=lambda: defaultdict(dict), init=False)
     
     def __post_init__(self):
         self.args_converted = Utils(args).modify_entry_params()
         self.get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
         self.get_headers = config.get('api').get('headers')
         self.params = config.get('api').get('params')
         self.start_date = self.args_converted["start_date"]
         self.end_date = self.args_converted["end_date"]

     def ingestion(self):
        connection_start_time = time.time()
        connection_timeout = 1
        day_range = int((datetime.fromisoformat(self.end_date) - datetime.fromisoformat(self.start_date)).days)+1
        loop_counter = 0
        
        while day_range > loop_counter:
            try:
                logger.info('From {cls} starting connection on Socrata API with attr: {attr}'.format(cls=self.params.__class__.__name__, attr=self.params), exc_info=True)

                connection = Socrata(url=self.get_url, headers=self.get_headers, parameters=self.params, start_date=self.start_date).api_connection()
                
                # print(json.dumps(connection.json(), indent=4))

                loop_counter += 1
                break 
            except TimeoutError:
                if time.time() > connection_start_time + connection_timeout:

                    logger.error('From {cls} unable to get connection after {attr} seconds of TimeoutError'.format(cls=type(connection_timeout).__name__, attr=connection_timeout))
                    
                    raise Exception('From {cls} unable to get connection after {attr} seconds of TimeoutError'.format(cls=type(connection_timeout).__name__, attr=connection_timeout))
                else:
                    logger.info('From {cls} starting retry logic every {attr} second'.format(cls=type(connection_timeout).__name__, attr=connection_timeout))

                    time.sleep(1)
            finally:
                logger.info("From {cls} ending connection on Socrata API with attr: {attr}".format(cls=type(connection).__name__, attr=connection.ok))

if __name__ == '__main__':
        Data