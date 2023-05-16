import logging
from data_ingestion import *

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
        Data().ingestion()