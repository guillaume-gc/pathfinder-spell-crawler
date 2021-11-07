import logging.config
import logging

from definitions import ROOT_DIR

logger = logging.getLogger('root')

logging.config.fileConfig(f'{ROOT_DIR}/pathfinder_spell_crawler/logging.conf')
