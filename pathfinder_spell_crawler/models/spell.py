from typing import Dict


class Spell:
    def __init__(self, data: Dict = None):
        if not data:
            data = {}

        self.source = data.get('source')

        self.school = data.get('school')
        self.sub_school = data.get('sub_school')
        self.descriptor = data.get('descriptor')

        self.casting_time = data.get('descriptor')

        try:
            components_data = data["components_data"]
            components_separator = components_data["separator"]
            components_string = components_data["value"]

            self.components = components_string.split(components_separator)
        except (KeyError, TypeError, ValueError):
            self.components = None

        self.casting_range = data.get('casting_range')

        self.target = data.get('target')
        self.duration = data.get('duration')
        self.save = data.get('save', {})
        self.spell_resistance = data.get('spell_resistance')

        self.description = data.get('description')
