import pytest
from deepdiff import DeepDiff

from mocking.mock_urllib import mock_urllib_request_response_wrapper
from utils.spell import get_spell_data


class TestSpellsListCrawler:
    @pytest.fixture(scope="class")
    def aonprd_pages(self):
        return [
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page.html',
                "url": 'https://aonprd.com/SpellDisplay.aspx?ItemName=Abadar%27s%20Truthtelling',
                "spell": get_spell_data('abadar_truthtelling')
            }
        ]

    @staticmethod
    def init_crawler(mocker, page):
        from pathfinder_spell_crawler.crawlers.spells.page.aonprd_spells_page_crawler import AonprdSpellPageCrawler

        mocker.patch('urllib.request', mock_urllib_request_response_wrapper(page["html_path"]))

        crawler = AonprdSpellPageCrawler(page["url"])

        crawler.get_spell_tag()

        return crawler

    @staticmethod
    def test_get_spell_aonprd_page_tag(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            assert crawler._tag is not None

    @staticmethod
    def test_get_spell_aonprd_page_name(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            name = crawler.get_name()
            assert name == page["spell"]["name"]

    @staticmethod
    def test_get_spell_aonprd_page_sources(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            sources = crawler.get_sources()
            assert not DeepDiff(sources, page["spell"]["sources"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_school(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            school = crawler.get_school()
            assert school == page["spell"]["school"]

    @staticmethod
    def test_get_spell_aonprd_page_sub_school(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            sub_school = crawler.get_sub_school()
            assert sub_school == page["spell"]["sub_school"]

    @staticmethod
    def test_get_spell_aonprd_page_descriptor(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            descriptor = crawler.get_descriptor()
            assert descriptor == page["spell"]["descriptor"]

    @staticmethod
    def test_get_spell_aonprd_page_casting_time(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            casting_time = crawler.get_casting_time()
            assert casting_time == page["spell"]["casting_time"]

    @staticmethod
    def test_get_spell_aonprd_page_levels(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            levels = crawler.get_levels()
            assert not DeepDiff(levels, page["spell"]["levels"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_components(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            components = crawler.get_components()
            assert not DeepDiff(components, page["spell"]["components"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_casting_range(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            casting_range = crawler.get_casting_range()
            assert casting_range == page["spell"]["casting_range"]

    @staticmethod
    def test_get_spell_aonprd_page_target(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            target = crawler.get_target()
            assert target == page["spell"]["target"]

    @staticmethod
    def test_get_spell_aonprd_page_duration(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            duration = crawler.get_duration()
            assert duration == page["spell"]["duration"]

    @staticmethod
    def test_get_spell_aonprd_page_save(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            save = crawler.get_save()
            assert save == page["spell"]["save"]

    @staticmethod
    def test_get_spell_aonprd_page_spell_resistance(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            spell_resistance = crawler.get_spell_resistance()
            assert spell_resistance == page["spell"]["spell_resistance"]

    @staticmethod
    def test_get_spell_aonprd_page_description(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsListCrawler.init_crawler(mocker, page)

            description = crawler.get_description()
            assert description == page["spell"]["description"]
