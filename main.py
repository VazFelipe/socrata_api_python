import json
import argparse
import logging.config
import time
from sys import argv
from datetime import date, datetime
from socrata import *
from utils import *

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
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

def main():
    args_converted = Utils(args).modify_entry_params()
    start_date = args_converted["start_date"]
    end_date = args_converted["end_date"]

    get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
    get_headers = config.get('api').get('headers')
    params = config.get('api').get('params')

    connection_start_time = time.time()
    connection_timeout = 1
    day_range = int((datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days)+1
    loop_counter = 0
    
    while day_range > loop_counter:
        try:
            logger.info("Starting connection on Socrata API with params: {}".format(params))

            connection = Socrata(url=get_url, headers=get_headers, parameters=params, start_date=start_date).api_connection()
            
            # print(json.dumps(connection.json(), indent=4))

            loop_counter += 1
            break 
        except ConnectionError:
            if time.time() > connection_start_time + connection_timeout:
                logger.error('Unable to get connection after {} seconds of ConnectionErrors'.format(connection_timeout))
                raise Exception('Unable to get connection after {} seconds of ConnectionErrors'.format(connection_timeout))
            else:
                 logger.info('Start retry logic every {} second'.format(connection_timeout))
                 time.sleep(1)
        finally:
            logger.info("Ending connection on Socrata API with response: {}".format(connection.ok))

if __name__ == '__main__':
        main()