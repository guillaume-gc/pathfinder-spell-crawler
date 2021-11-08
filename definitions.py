import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DICT = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
        }
    },
    "handlers": {
        "console": {
            "level": 'INFO',
            "formatter": 'standard',
            "class": 'logging.StreamHandler'
        }
    },
    "loggers": {
        "": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": True
        },
        "app": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": False
        }
    }
}

