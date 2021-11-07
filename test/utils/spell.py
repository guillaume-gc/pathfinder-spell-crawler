import json


def get_spell_data(spell_name: str) -> dict:
    from definitions import ROOT_DIR

    spell_file_path = f'{ROOT_DIR}/test/samples/spells/{spell_name}.json'

    with open(spell_file_path, 'r') as file:
        return json.load(file)
