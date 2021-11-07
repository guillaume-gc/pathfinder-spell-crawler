import urllib.request
from typing import List

from bs4 import BeautifulSoup


class SpellsListCrawler:
    def __init__(self, url, spell_pages_html_descriptor):
        self.url = url
        self.spell_pages_html_descriptor = spell_pages_html_descriptor

    def get_spell_html_pages(self) -> List[str]:
        html_global_text = self._get_html_text()

        soup = BeautifulSoup(html_global_text, 'html.parser')

        return soup.find_all(self.spell_pages_html_descriptor)

    def _get_html_text(self) -> str:
        page = urllib.request.urlopen(self.url)

        return page.read().decode('utf8')
