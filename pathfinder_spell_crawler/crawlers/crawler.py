import urllib.request
import urllib.parse

from pathfinder_spell_crawler.util import url_tools


class Crawler:
    def __init__(self, url):
        self._url = url
        self._domain = url_tools.get_domain(url)

    def _get_html_text(self) -> str:
        page = urllib.request.urlopen(self._url)

        return page.read().decode('utf8')

    def _create_link_from_relative_path(self, relative_path: str):
        return self._domain + urllib.parse.quote(relative_path, safe='?=()')
