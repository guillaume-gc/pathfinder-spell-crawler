import logging.config
import logging
import os
import sys

import pytest

logger = None


@pytest.fixture(scope="session", autouse=True)
def init_path():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'
    sys.path.insert(0, root_dir)


@pytest.fixture(scope="session", autouse=True)
def init_logging():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'

    logging.config.fileConfig(f'{root_dir}/test/logging.conf')

    global logger
    logger = logging.getLogger('root')
