import pytest
from deepdiff import DeepDiff

from mocking.mock_urllib import mock_urllib_request_response_wrapper
from utils.spell import get_spell_data


class TestSpellsPageCrawler:
    @pytest.fixture(scope="class")
    def aonprd_pages(self):
        return [
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_abadar_truthtelling.html',
                "url": 'https://aonprd.com/SpellDisplay.aspx?ItemName=Abadar%27s%20Truthtelling',
                "spell": get_spell_data('abadar_truthtelling')
            },
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_abeyance.html',
                "url": 'https://aonprd.com/SpellDisplay.aspx?ItemName=Abeyance',
                "spell": get_spell_data('abeyance')
            },
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_abjuring_step.html',
                "url": 'https://aonprd.com/SpellDisplay.aspx?ItemName=Abjuring%20Step',
                "spell": get_spell_data('abjuring_step')
            },
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_absorb_rune_2.html',
                "url": 'https://aonprd.com/SpellDisplay.aspx?ItemName=Absorb%20Rune%20II',
                "spell": get_spell_data('absorb_rune_2')
            },
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_absorbing_barrier.html',
                "url": 'https://www.aonprd.com/SpellDisplay.aspx?ItemName=Absorbing%20Barrier',
                "spell": get_spell_data('absorbing_barrier')
            },
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_curse_of_dragonflies.html',
                "url": 'https://aonprd.com/SpellDisplay.aspx?ItemName=Curse%20of%20Dragonflies',
                "spell": get_spell_data('curse_of_dragonflies')
            },
            {
                "html_path": '/test/samples/fake_page/aonprd_spell_page_curse_terrain.html',
                "url": 'https://www.aonprd.com/SpellDisplay.aspx?ItemName=Curse%20Terrain',
                "spell": get_spell_data('curse_terrain')
            }
        ]

    @staticmethod
    def init_crawler(mocker, page):
        from pathfinder_spell_crawler.crawlers.spells.page.aonprd_spells_page_crawler import AonprdSpellPageCrawler

        mocker.patch('urllib.request', mock_urllib_request_response_wrapper(page["html_path"]))

        crawler = AonprdSpellPageCrawler(page["spell"]["name"], page["url"])

        crawler.update_spell_tag()

        return crawler

    @staticmethod
    def test_get_spell_aonprd_page_tag(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            assert crawler._tag is not None

    @staticmethod
    def test_get_spell_aonprd_page_name(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            name = crawler.get_name()
            assert name == page["spell"]["name"]

    @staticmethod
    def test_get_spell_aonprd_page_sources(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            sources = crawler.get_sources()
            assert not DeepDiff(sources, page["spell"]["sources"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_school(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            school = crawler.get_school()
            assert school == page["spell"]["school"]

    @staticmethod
    def test_get_spell_aonprd_page_sub_school(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            sub_school = crawler.get_sub_school()
            assert sub_school == page["spell"]["sub_school"]

    @staticmethod
    def test_get_spell_aonprd_page_descriptors(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            descriptors = crawler.get_descriptors()
            assert not DeepDiff(descriptors, page["spell"]["descriptors"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_casting_time(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            casting_time = crawler.get_casting_time()
            assert casting_time == page["spell"]["casting_time"]

    @staticmethod
    def test_get_spell_aonprd_page_levels(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            levels = crawler.get_levels()
            assert not DeepDiff(levels, page["spell"]["levels"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_components(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            components = crawler.get_components()
            assert not DeepDiff(components, page["spell"]["components"], ignore_order=True)

    @staticmethod
    def test_get_spell_aonprd_page_casting_range(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            casting_range = crawler.get_casting_range()
            assert casting_range == page["spell"]["casting_range"]

    @staticmethod
    def test_get_spell_aonprd_page_target(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            target = crawler.get_target()
            assert target == page["spell"]["target"]

    @staticmethod
    def test_get_spell_aonprd_page_area(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            target = crawler.get_area()
            assert target == page["spell"]["area"]

    @staticmethod
    def test_get_spell_aonprd_page_effect(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            target = crawler.get_effect()
            assert target == page["spell"]["effect"]

    @staticmethod
    def test_get_spell_aonprd_page_duration(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            duration = crawler.get_duration()
            assert duration == page["spell"]["duration"]

    @staticmethod
    def test_get_spell_aonprd_page_save(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            save = crawler.get_save()
            assert save == page["spell"]["save"]

    @staticmethod
    def test_get_spell_aonprd_page_spell_resistance(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            spell_resistance = crawler.get_spell_resistance()
            assert spell_resistance == page["spell"]["spell_resistance"]

    @staticmethod
    def test_get_spell_aonprd_page_description(mocker, aonprd_pages):
        for page in aonprd_pages:
            crawler = TestSpellsPageCrawler.init_crawler(mocker, page)

            description = crawler.get_description()
            assert description == page["spell"]["description"]
