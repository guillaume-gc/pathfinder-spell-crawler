from bs4 import BeautifulSoup

from pathfinder_spell_crawler.crawlers.spells.list.spells_list_crawler import SpellsListCrawler


class AonprdSpellsListCrawler(SpellsListCrawler):
    def __init__(self, url):
        super().__init__(url)

    def get_spell_result_set(self):
        html_global_text = self._get_html_text()

        soup = BeautifulSoup(html_global_text, 'html.parser')

        # See test/samples/fake_page/aonprd_spell_list.html for a HTML sample.
        return soup.find(id='main').find('table').find_all('td')

    def extract_spell_link_from_tag(self, tag):
        return self._create_link_from_relative_path(tag.span.b.a['href'])
