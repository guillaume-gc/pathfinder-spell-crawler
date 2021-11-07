import os
import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def init_path():
    root_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'
    sys.path.insert(0, root_dir)
