import pytest

from mocking.mock_urllib import mock_urllib_request_response_wrapper


class TestSpellsListCrawler:
    @pytest.fixture(scope="class")
    def pages(self):
        return [
            {
                "url": 'https://aonprd.com/Spells.aspx?Class=All',
                "html_path": '/test/samples/fake_page/aonprd_spells_list.html',
                "spell_pages_html_descriptor": 'td',
                "expected_pages": 12
            }
        ]

    @staticmethod
    def test_get_spell_pages(mocker, pages):
        from pathfinder_spell_crawler.crawlers.spells_list_crawler import SpellsListCrawler

        for page in pages:
            mocker.patch('urllib.request', mock_urllib_request_response_wrapper(page["html_path"]))

            crawler = SpellsListCrawler(page["url"], page["spell_pages_html_descriptor"])
            pages = crawler.get_spell_html_pages()

            assert len(pages) == page["expected_pages"]
