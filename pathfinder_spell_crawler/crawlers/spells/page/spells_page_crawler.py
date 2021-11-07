import abc

from bs4 import BeautifulSoup

from pathfinder_spell_crawler.crawlers.crawler import Crawler


class SpellPageCrawler(Crawler, abc.ABC):
    def __init__(self, url):
        super().__init__(url)

        self.tag = None

    def get_spell_tag(self):
        html_global_text = self._get_html_text()

        soup = BeautifulSoup(html_global_text, 'html.parser')

        # See test/samples/fake_page/aonprd_spell_page.html for a HTML sample.
        return soup.find(id='main').find('table').find_all('td')

    @abc.abstractmethod
    def get_source(self):
        raise NotImplemented('method get_source not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_school(self):
        raise NotImplemented('method get_school not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_sub_school(self):
        raise NotImplemented('method get_sub_school not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_casting_time(self):
        raise NotImplemented('method get_casting_time not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_components(self):
        raise NotImplemented('method get_components not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_casting_range_descriptor(self):
        raise NotImplemented('method get_casting_range_descriptor not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_target(self):
        raise NotImplemented('method get_target not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_duration(self):
        raise NotImplemented('method get_duration not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_save(self):
        raise NotImplemented('method get_save not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_spell_resistance(self):
        raise NotImplemented('method get_spell_resistance not implemented for SpellPageCrawler class')

    @abc.abstractmethod
    def get_description(self):
        raise NotImplemented('method get_description not implemented for SpellPageCrawler class')
