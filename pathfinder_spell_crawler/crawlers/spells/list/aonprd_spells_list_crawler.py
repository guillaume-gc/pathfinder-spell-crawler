from typing import Tuple

from bs4 import BeautifulSoup

from pathfinder_spell_crawler.crawlers.spells.list import logger
from pathfinder_spell_crawler.crawlers.spells.list.spells_list_crawler import SpellsListCrawler


class AonprdSpellsListCrawler(SpellsListCrawler):
    def __init__(self, url):
        super().__init__(url)

    def get_spell_result_set(self):
        logger.info(f'Get Spell Result Set: URL is "{self._url}".')

        html_global_text = self._get_html_text()
        logger.info(f'Get Spell Result Set: HTML extracted.')
        logger.debug(html_global_text)

        soup = BeautifulSoup(html_global_text, 'html.parser')
        logger.info(f'Get Spell Result Set: Soup created from HTML.')

        # See test/samples/fake_page/aonprd_spell_list.html for a HTML sample.
        result_set = soup.find(id='main').find('table').find_all('td')
        logger.info(f'Get Spell Result Set: Result Set Created from Soup.')
        logger.debug(str(result_set))

        return result_set

    def extract_spell_data_from_tag(self, tag) -> Tuple[str, str]:
        logger.debug(f'Extract Spell Data from Tag: Ready.')
        logger.debug(tag)

        href = tag.span.b.a['href']
        logger.debug(f'Extract Spell Data from Tag: HRef is "{href}"')

        url = self._create_url_from_relative_path(href)
        logger.debug(f'Extract Spell Data from Tag: Complete URL is "{url}"')

        name = tag.b.text.strip()
        logger.debug(f'Extract Spell Data from Tag: Name is "{name}"')

        return name, url
