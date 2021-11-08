import time
from typing import List, Dict

from pathfinder_spell_crawler.crawlers.controller import logger
from pathfinder_spell_crawler.crawlers.controller.crawler_controller import CrawlerController, PAGINATION_SLEEP_TIME
from pathfinder_spell_crawler.crawlers.spells.list.aonprd_spells_list_crawler import AonprdSpellsListCrawler
from pathfinder_spell_crawler.crawlers.spells.page.aonprd_spells_page_crawler import AonprdSpellPageCrawler
from pathfinder_spell_crawler.models.spell_model import SpellModel


class AonprdCrawlerController(CrawlerController):
    def __init__(self, url):
        super().__init__(url)

        self.spells_list_crawler = AonprdSpellsListCrawler(self._url)
        self.spells_page_crawlers = []
        self.spell_models = []

    def create_all_page_crawlers(self) -> List[AonprdSpellPageCrawler]:
        logger.info('Create all Page Crawlers: Ready.')

        logger.info('Create all Page Crawlers: Remove any existing Page Crawler.')
        self.spells_page_crawlers = []

        logger.info('Create all Page Crawlers: Obtaining Page Crawler.')
        result_set = self.spells_list_crawler.get_spell_result_set()
        data = self.spells_list_crawler.extract_spell_data_from_result_set(result_set)

        logger.info(f'Create all Page Crawlers: {len(data)} spells obtained from List Crawler.')

        for e in data:
            # Let us not DDOS the website.
            time.sleep(PAGINATION_SLEEP_TIME)

            spells_page_crawler = AonprdSpellPageCrawler(e["name"], e["url"])
            self.spells_page_crawlers.append(spells_page_crawler)

            logger.debug(f'Create all Page Crawler: Created Page Crawler from name "{e["name"]}" URL "{e["url"]}"')

        logger.info(f'Create all Page Crawlers: All {len(data)} spells translated into Page Crawlers.')

        return self.spells_page_crawlers

    def get_spell_models_from_page_crawlers(self) -> List[SpellModel]:
        self.spell_models = []

        for crawler in self.spells_page_crawlers:
            spell_model = AonprdCrawlerController._get_spell_model_from_page_crawler(crawler)
            self.spell_models.append(spell_model)

        return self.spell_models

    def get_spells_model_json(self) -> List[Dict]:
        spell_models_json = []

        for model in self.spell_models:
            spell_models_json.append(model.__dict__)

        return spell_models_json

    @staticmethod
    def _get_spell_model_from_page_crawler(page_crawler: AonprdSpellPageCrawler) -> SpellModel:
        page_crawler.update_spell_tag()
        spell_model = SpellModel()

        spell_model.set_data_from_page_crawler(page_crawler)

        return spell_model
