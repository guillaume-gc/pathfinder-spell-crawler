from typing import List

from bs4 import BeautifulSoup

from pathfinder_spell_crawler.crawlers.spells.list.spells_list_crawler import SpellsListCrawler


class AonprdSpellsListCrawler(SpellsListCrawler):
    def get_spell_result_set(self):
        spell_list_html_descriptor = 'td'
        html_global_text = self._get_html_text()

        soup = BeautifulSoup(html_global_text, 'html.parser')

        return soup.find_all(spell_list_html_descriptor)

    def extract_spell_link_from_tag(self, tag):
        return tag.span.b.a['href']
