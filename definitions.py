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
        }
    },
    "loggers": {
        "": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": False
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
        },
        "crawlers.controller": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers.spells.list": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": False
        },
        "crawlers.spells.page": {
            "handlers": ['console'],
            "level": 'DEBUG',
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
        'cursed',
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
