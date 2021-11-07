import pytest
from deepdiff import DeepDiff

from mocking.mock_urllib import mock_urllib_request_response_wrapper


class TestSpellsListCrawler:
    @pytest.fixture()
    def aonprd_pages(self):
        return [
            {
                "html_path": '/test/samples/fake_page/aonprd_spells_list_small.html',
                "spell_links": [
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Abadar%27s%20Truthtelling',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Abeyance',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Abjuring%20Step',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Ablative%20Barrier',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Ablative%20Sphere%20(Garundi)',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Aboleth%27s%20Lung',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Absolution',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Absorb%20Rune%20I',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Absorb%20Rune%20II',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Absorb%20Rune%20III',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Absorb%20Toxicity',
                    'https://aonprd.com/SpellDisplay.aspx?ItemName=Absorbing%20Barrier'
                ]
            }
        ]

    @staticmethod
    def test_get_spell_aonprd_pages_small_count(mocker, aonprd_pages):
        from pathfinder_spell_crawler.crawlers.spells.list.aonprd_spells_list_crawler import AonprdSpellsListCrawler

        url = 'https://aonprd.com/Spells.aspx?Class=All'

        for page in aonprd_pages:
            mocker.patch('urllib.request', mock_urllib_request_response_wrapper(page["html_path"]))

            crawler = AonprdSpellsListCrawler(url)
            result_set = crawler.get_spell_result_set()

            assert len(result_set) == len(page["spell_links"])

    @staticmethod
    def test_get_spell_aonprd_pages_small_links(mocker, aonprd_pages):
        from pathfinder_spell_crawler.crawlers.spells.list.aonprd_spells_list_crawler import AonprdSpellsListCrawler

        url = 'https://aonprd.com/Spells.aspx?Class=All'

        for page in aonprd_pages:
            mocker.patch('urllib.request', mock_urllib_request_response_wrapper(page["html_path"]))

            crawler = AonprdSpellsListCrawler(url)
            result_set = crawler.get_spell_result_set()

            links = crawler.extract_spell_links_from_result_set(result_set)

            assert not DeepDiff(links, page["spell_links"], ignore_order=True)
