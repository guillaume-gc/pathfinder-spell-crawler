import re
from typing import List

from bs4 import BeautifulSoup

from pathfinder_spell_crawler.crawlers.crawler import Crawler
from pathfinder_spell_crawler.crawlers import logger
from pathfinder_spell_crawler.crawlers.exceptions.spells_page_crawling_exception import SpellsPageCrawlingException


class AonprdSpellPageCrawler(Crawler):
    def __init__(self, url):
        super().__init__(url)

        self._tag = None

    def get_spell_tag(self):
        logger.info(f'Get Spell Tag: URL is "{self._url}"')

        html_global_text = self._get_html_text()
        logger.info(f'Get Spell Tag: HTML extracted.')
        logger.debug(html_global_text)

        soup = BeautifulSoup(html_global_text, 'html.parser')
        logger.info(f'Get Spell Tag: HTML extracted.')

        # See test/samples/fake_page/aonprd_spell_page.html for a HTML sample.
        self._tag = soup.find(id='main').find('table').tr.td.span
        logger.info(f'Get Spell Tag: Tag Created from Soup.')
        logger.debug(self._tag)

    def get_name(self) -> str:
        logger.debug('Get Name: Ready.')

        if self._tag is None:
            logger.error('Get Name: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'name')

        try:
            name = self._tag.find('h1', class_='title').text

            # Remove any whitespace and line break before and after the name.
            name = name.strip()

            logger.debug(f'Get Name: Value is {name}.')

            return name
        except Exception as ex:
            logger.exception(f'Get Name: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'name')

    def get_sources(self) -> List[str]:
        logger.debug('Get Sources: Ready.')

        if self._tag is None:
            logger.error('Get Sources: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'sources')

        try:
            sources = []

            source_title = self._tag.find('b', text='Source')
            source_title_next_siblings = source_title.find_next_siblings()

            for sibling in source_title_next_siblings:
                if str(sibling) == '<br/>':
                    break
                if sibling.name == 'a':
                    source = sibling.text
                    source = source.strip()
                    sources.append(source)

            logger.debug(f'Get Sources: Values are {sources}.')

            return sources
        except Exception as ex:
            logger.exception(f'Get Sources: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'sources')

    def get_school(self):
        logger.debug('Get School: Ready.')

        if self._tag is None:
            logger.error('Get Sources: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'school')

        try:
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()

            # Normally there is always at least one sibling: the main school.
            school = siblings[0].find('a').text
            school = school.strip().capitalize()

            logger.debug(f'Get School: Value is {school}.')

            return school
        except Exception as ex:
            logger.exception(f'Get School: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'school')

    def get_sub_school(self):
        logger.debug('Get Sub School: Ready.')

        if self._tag is None:
            logger.error('Get Sub School: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'sub_school')

        try:
            # Sub School is part of school and is optional.
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()
            try:
                sub_school = siblings[1].find('a').text
                sub_school = sub_school.strip().capitalize()
            except IndexError:
                logger.debug(f'Get Sub School: Value not found but is optional. Set it to empty')
                sub_school = ''

            logger.debug(f'Get Sub School: Value is {sub_school}.')

            return sub_school
        except Exception as ex:
            logger.exception(f'Get Sub School: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'sub_school')

    def get_descriptor(self):
        logger.debug('Get Descriptor: Ready.')

        if self._tag is None:
            logger.error('Get Descriptor: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'descriptor')

        try:
            # Descriptor part of school and is optional.
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()

            try:
                descriptor = siblings[2].find('a').text
                descriptor = descriptor.strip().capitalize()
            except IndexError:
                logger.debug(f'Get Descriptor: Value not found but is optional. Set it to empty')
                descriptor = ''

            logger.debug(f'Get Descriptor: Value is {descriptor}.')

            return descriptor
        except Exception as ex:
            logger.exception(f'Get Descriptor: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'descriptor')

    def get_levels(self):
        logger.debug('Get Levels: Ready.')

        if self._tag is None:
            logger.error('Get Levels: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'levels')

        try:
            levels_title = self._tag.find('b', text='Level')

            # By default, BeautifulSoup only works with named elements (such as <a>), not simple text.
            # This can be changed using string argument, with a regex containing all possible strings.
            siblings = levels_title.find_next_siblings(string=re.compile("."))

            levels_string = siblings[0]

            levels = levels_string.split(',')
            levels = [level.strip().capitalize() for level in levels]

            logger.debug(f'Get Levels: Values are {levels}.')

            return levels
        except Exception as ex:
            logger.exception(f'Get Levels: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'levels')

    def get_casting_time(self):
        logger.debug('Get Casting Time: Ready.')

        if self._tag is None:
            logger.error('Get Casting Time: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'casting_time')

        try:
            casting_time_title = self._tag.find('b', text='Casting Time')

            siblings = casting_time_title.find_next_siblings(string=re.compile("."))

            casting_time = siblings[0]
            casting_time = casting_time.strip().capitalize()

            logger.debug(f'Get Casting Time: Value is {casting_time}.')

            return casting_time
        except Exception as ex:
            logger.exception(f'Get Casting Time: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'casting_time')

    def get_components(self):
        logger.debug('Get Components: Ready.')

        if self._tag is None:
            logger.error('Get Components: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'components')

        try:
            components_title = self._tag.find('b', text='Components')

            siblings = components_title.find_next_siblings(string=re.compile("."))

            components_string = siblings[0]

            components = components_string.split(',')
            components = [component.strip().upper() for component in components]

            logger.debug(f'Get Components: Values are {components}.')

            return components
        except Exception as ex:
            logger.exception(f'Get Components: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'casting_time')

    def get_casting_range(self):
        logger.debug('Get Casting Range: Ready.')

        if self._tag is None:
            logger.error('Get Casting Range: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'casting_range')

        try:
            casting_range_title = self._tag.find('b', text='Range')

            siblings = casting_range_title.find_next_siblings(string=re.compile("."))

            casting_range = siblings[0]
            casting_range = casting_range.strip().capitalize()

            logger.debug(f'Get Casting Range: Value is {casting_range}.')

            return casting_range
        except Exception as ex:
            logger.exception(f'Get Casting Range: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'casting_range')

    def get_target(self):
        logger.debug('Get Target: Ready.')

        if self._tag is None:
            logger.error('Get Target: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'target')

        try:
            target_title = self._tag.find('b', text='Target')

            siblings = target_title.find_next_siblings(string=re.compile("."))

            target = siblings[0]
            target = target.strip().capitalize()

            logger.debug(f'Get Target: Value is {target}.')

            return target
        except Exception as ex:
            logger.exception(f'Get Target: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'target')

    def get_duration(self):
        logger.debug('Get Duration: Ready.')

        if self._tag is None:
            logger.error('Get Duration: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'duration')

        try:
            duration_title = self._tag.find('b', text='Duration')

            siblings = duration_title.find_next_siblings(string=re.compile("."))

            duration = siblings[0]
            duration = duration.strip().capitalize()

            logger.debug(f'Get Duration: Value is {duration}.')

            return duration
        except Exception as ex:
            logger.exception(f'Get Duration: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'duration')

    def get_save(self):
        logger.debug('Get Save: Ready.')

        if self._tag is None:
            logger.error('Get Save: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'save')

        try:
            save_title = self._tag.find('b', text='Saving Throw')

            siblings = save_title.find_next_siblings(string=re.compile("."))

            save = siblings[0]
            save = save.strip().capitalize().replace(';', '')

            logger.debug(f'Get Save: Value is {save}.')

            return save
        except Exception as ex:
            logger.exception(f'Get Save: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'save')

    def get_spell_resistance(self):
        logger.debug('Get Spell Resistance: Ready.')

        if self._tag is None:
            logger.error('Get Spell Resistance: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'spell_resistance')

        try:
            spell_resistance_title = self._tag.find('b', text='Spell Resistance')

            siblings = spell_resistance_title.find_next_siblings(string=re.compile("."))

            spell_resistance = siblings[0]
            spell_resistance = spell_resistance.strip().capitalize()

            logger.debug(f'Get Spell Resistance: Value is {spell_resistance}.')

            return spell_resistance
        except Exception as ex:
            logger.exception(f'Get Save: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'spell_resistance')

    def get_description(self):
        logger.debug('Get Description: Ready.')

        if self._tag is None:
            logger.error('Get Description: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', 'description')

        try:
            description_title = self._tag.find('h3', class_='framing', text='Description')

            # Descriptions are made with sub elements, line breaks and so on and so forth, so there are multiple texts.
            sibling = description_title.next_sibling
            description_list = []
            while sibling:
                description_list.append(sibling.text)
                sibling = sibling.next_sibling

            description = ''.join(description_list)
            description = description.strip()

            logger.debug(f'Get Description: Value is "{description}".')

            return description
        except Exception as ex:
            logger.exception(f'Get Description: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', 'description')
