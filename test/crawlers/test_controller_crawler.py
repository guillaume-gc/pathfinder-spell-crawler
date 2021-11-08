import pytest

from mocking.mock_urllib import mock_urllib_request_response_wrapper


class TestSpellsListCrawler:
    @pytest.fixture(scope="class")
    def aonprd_pages(self):
        return [
            {
                "html_path": '/test/samples/fake_page/aonprd_spells_list_small.html',
                "url": 'https://aonprd.com/Spells.aspx?Class=All',
                "spell_urls": [
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
    def test_aonprd_crawler_create_all_page_crawlers_small_count(mocker, aonprd_pages):
        from pathfinder_spell_crawler.crawlers.controller.aonprd_crawler_controller import AonprdCrawlerController

        for page in aonprd_pages:
            mocker.patch('urllib.request', mock_urllib_request_response_wrapper(page["html_path"]))

            crawler = AonprdCrawlerController(page["url"])
            spells_page_crawlers = crawler.create_all_page_crawlers()

            assert len(spells_page_crawlers) == len(page["spell_urls"])
