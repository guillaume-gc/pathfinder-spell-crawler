import json
from time import time

from definitions import ROOT_DIR
from pathfinder_spell_crawler.app import logger
from pathfinder_spell_crawler.crawlers.controller.aonprd_crawler_controller import AonprdCrawlerController


def main():
    logger.info(f'Main: Begin.')

    crawler_controller = AonprdCrawlerController('https://aonprd.com/Spells.aspx?Class=All')

    crawler_controller.create_all_page_crawlers()
    spells_models = crawler_controller.get_spell_models_from_page_crawlers()

    logger.info(f'Main: {len(spells_models)} spells obtained.')

    spell_models_dict = crawler_controller.get_spells_model_json()

    current_timestamp = int(time())
    file_path = f'{ROOT_DIR}/data/spells-{current_timestamp}.json'
    with open(file_path, 'w') as file:
        file.write(json.dumps(spell_models_dict))

    logger.info(f'Main: File {file_path} created.')


if __name__ == '__main__':
    main()
