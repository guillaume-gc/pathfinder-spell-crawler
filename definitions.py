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
            "formatter": 'standard',
            "class": 'logging.StreamHandler'
        },
        "file_last_run_default": {
            "formatter": 'standard',
            "class": 'logging.FileHandler',
            "filename": f'{ROOT_DIR}/data/last_run_default.log',
            "mode": 'w',
            "encoding": 'utf-8'
        },
        "file_last_warning": {
            "formatter": 'standard',
            "class": 'logging.FileHandler',
            "filename": f'{ROOT_DIR}/data/last_run_warning.log',
            "mode": 'w',
            "level": "WARNING",
            "encoding": 'utf-8'
        }
    },
    "loggers": {
        "": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        },
        "app": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers.controller": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers.spells.list": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers.spells.page": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        },
        "soup": {
            "handlers": ['console', 'file_last_run_default', 'file_last_warning'],
            "level": 'INFO',
            "propagate": False
        }
    }
}
WHITELIST = {
    "descriptors": [
        'acid',
        'air',
        'chaotic',
        'cold',
        'curse',
        'darkness',
        'death',
        'disease',
        'draconic',
        'earth',
        'electricity',
        'emotion',
        'evil',
        'fear',
        'fire',
        'force',
        'good',
        'language-dependent',
        'lawful',
        'light',
        'meditative',
        'mind-affecting',
        'pain',
        'poison',
        'ruse',
        'shadow',
        'sonic',
        'water'
    ],
    "sub_schools": [
        'calling',
        'charm',
        'compulsion',
        'creation',
        'figment',
        'glamer',
        'haunted',
        'healing',
        'pattern',
        'phantasm',
        'polymorph',
        'scrying',
        'shadow',
        'summoning',
        'teleportation'
    ],
    'schools': [
        'abjuration',
        'conjuration',
        'divination',
        'enchantment',
        'evocation',
        'illusion',
        'necromancy',
        'transmutation',
        'universal'
    ]
}
