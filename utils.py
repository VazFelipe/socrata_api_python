import logging
from datetime import timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Utils():
    args_dict: dict

    def modify_entry_params(self):

            for key, value in self.args_dict.items():            
                if key.endswith("date"):            
                    args_dict_updated = {key: (value + timedelta(days=0, hours=23, minutes=59, seconds=59, microseconds=999999)).isoformat()}
                    self.args_dict.update(args_dict_updated)

            logger.info('From {cls} the attr: {attr}'.format(cls=type(self.args_dict).__name__, attr=self.args_dict), exc_info=True)

            return self.args_dict

if __name__ == '__main__':
    Utils