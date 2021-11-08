import logging.config
import logging

from definitions import LOG_DICT

logger = logging.getLogger('root')

logging.config.dictConfig(LOG_DICT)
