import abc

from typing import List, Dict

from pathfinder_spell_crawler.crawlers.crawler import Crawler
from pathfinder_spell_crawler.crawlers.spells.list import logger


class SpellsListCrawler(Crawler, abc.ABC):
    def __init__(self, url):
        super().__init__(url)

    @abc.abstractmethod
    def get_spell_result_set(self) -> List[str]:
        raise NotImplemented('method get_spell_html_pages not implemented for SpellsListCrawler class')

    @abc.abstractmethod
    def extract_spell_data_from_tag(self, html_tag):
        raise NotImplemented('method extract_spell_link_from_tag not implemented for SpellsListCrawler class')

    def extract_spell_data_from_result_set(self, result_set) -> List[Dict]:
        logger.info('Extract Spell Data: Ready.')
        data = []

        for tag in result_set:
            name, url = self.extract_spell_data_from_tag(tag)
            data.append({
                "name": name,
                "url": url
            })

        logger.info(f'Extract Spell Data: Found {len(data)} spells.')

        return data
