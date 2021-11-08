import re
from typing import List

from bs4 import BeautifulSoup

from definitions import WHITELIST
from pathfinder_spell_crawler.crawlers.crawler import Crawler
from pathfinder_spell_crawler.crawlers.exceptions.spells_page_crawling_exception import SpellsPageCrawlingException
from pathfinder_spell_crawler.crawlers.spells.page import logger


class AonprdSpellPageCrawler(Crawler):
    def __init__(self, spell_name, url):
        super().__init__(url)

        self._tag = None
        self._spell_name = spell_name

    def update_spell_tag(self):
        self._tag = None

        logger.info(f'Update {self._spell_name} Spell Tag: URL is "{self._url}"')

        html_global_text = self._get_html_text()
        logger.info(f'Update {self._spell_name} Spell Tag: HTML extracted.')
        logger.debug(html_global_text)

        soup = BeautifulSoup(html_global_text, 'html.parser')
        logger.info(f'Update {self._spell_name} Spell Tag: Soup created from HTML.')

        # See test/samples/fake_page/aonprd_spell_page_abadar_truthtelling.html for a HTML sample.
        td_result_set = soup.find(id='main').find('table').find_all('td')

        logger.info(f'Update {self._spell_name} Spell Tag: {len(td_result_set)} spells found.')

        for tag in td_result_set:
            try:
                current_spell_name = tag.span.h1.text.strip()

                logger.debug(f'Update {self._spell_name} Spell Tag: "{current_spell_name}" spell found.')

                if current_spell_name == self._spell_name:
                    logger.info(f'Update {self._spell_name} Spell Tag: Found correct spell.')
                    self._tag = tag
                    break
            # If an error related to a missing HTML field happens, ignore it.
            except AttributeError as ex:
                logger.debug(f'Update {self._spell_name} Spell Tag: {type(ex).__name__} -> {ex}.')
                pass

        logger.debug(self._tag)

        if self._tag is None:
            logger.error(f'Update {self._spell_name} Spell Tag: Could not find spell.')
            raise SpellsPageCrawlingException('spell not found', self._spell_name)

    def get_name(self) -> str:
        logger.debug(f'{self._spell_name} Get Name: Ready.')

        if self._tag is None:
            logger.error('Get Name: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'name')

        try:
            name = self._tag.find('h1', class_='title').text

            # Remove any whitespace and line break before and after the name.
            name = name.strip()

            logger.info(f'Get Name: Value is {name}.')

            return name
        except Exception as ex:
            logger.exception(f'Get Name: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'name')

    def get_sources(self) -> List[str]:
        logger.debug(f'{self._spell_name} Get Sources: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Sources: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'sources')

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

            logger.info(f'{self._spell_name} Get Sources: Values are {sources}.')

            return sources
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Sources: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'sources')

    def get_school(self):
        logger.debug(f'{self._spell_name} Get School: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Sources: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'school')

        try:
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()

            # Normally there is always at least one sibling: the main school.
            school = siblings[0].find('a').text
            school = school.strip().capitalize()

            logger.info(f'{self._spell_name} Get School: Value is {school}.')

            return school
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get School: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'An {ex} error occurred', self._spell_name, 'school')

    def get_sub_school(self):
        logger.debug(f'{self._spell_name} Get Sub School: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Sub School: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'sub_school')

        try:
            # Sub School is part of school and is optional.
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()
            sub_school = ''

            try:
                for sibling in siblings:
                    text = sibling.find('a').text.strip()

                    if text == '':
                        continue
                    if text in WHITELIST['sub_schools']:
                        sub_school = text.capitalize()
                        break
                        # Check other possible fields values to see if it's an unknown value
                    if text not in WHITELIST['descriptors'] and text not in WHITELIST['schools']:
                        logger.warning(f'{self._spell_name} Get Sub School: Unknown value found, is {text}')
            except (IndexError, AttributeError) as ex:
                logger.debug(f'Get Sub School: Error {type(ex).__name__} -> {ex}. Since is optional, ignore it.')

            logger.info(f'{self._spell_name} Get Sub School: Value is {sub_school}.')

            return sub_school
        except Exception as ex:
            logger.exception(f'Get Sub School: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'sub_school')

    def get_descriptor(self):
        logger.debug(f'{self._spell_name} Get Descriptor: Ready.')

        if self._tag is None:
            logger.error('Get Descriptor: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'descriptor')

        try:
            # Descriptor part of school and is optional.
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()
            descriptor = ''

            try:
                for sibling in siblings:
                    text = sibling.find('a').text.strip()

                    if text == '':
                        continue
                    if text in WHITELIST['descriptors']:
                        descriptor = text.capitalize()
                        break
                    # Check other possible fields values to see if it's an unknown value
                    if text not in WHITELIST['sub_schools'] and text not in WHITELIST['schools']:
                        logger.warning(f'Get Descriptor: Unknown value found, is {text}')
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self._spell_name} Get Descriptor: Error {type(ex).__name__} -> {ex}. '
                             f'Since is optional, ignore it.')

            logger.info(f'{self._spell_name} Get Descriptor: Value is {descriptor}.')

            return descriptor
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Descriptor: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'descriptor')

    def get_levels(self):
        logger.debug('Get Levels: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Levels: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'levels')

        try:
            levels_title = self._tag.find('b', text='Level')

            # By default, BeautifulSoup only works with named elements (such as <a>), not simple text.
            # This can be changed using string argument, with a regex containing all possible strings.
            siblings = levels_title.find_next_siblings(string=re.compile("."))

            levels_string = siblings[0]

            levels = levels_string.split(',')
            levels = [level.strip().capitalize() for level in levels]

            logger.info(f'{self._spell_name} Get Levels: Values are {levels}.')

            return levels
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Levels: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'levels')

    def get_casting_time(self):
        logger.debug(f'{self._spell_name} Get Casting Time: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Casting Time: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'casting_time')

        try:
            casting_time_title = self._tag.find('b', text='Casting Time')

            siblings = casting_time_title.find_next_siblings(string=re.compile("."))

            casting_time = siblings[0]
            casting_time = casting_time.strip().capitalize()

            logger.info(f'{self._spell_name} Get Casting Time: Value is {casting_time}.')

            return casting_time
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Casting Time: '
                             f'An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'casting_time')

    def get_components(self):
        logger.debug(f'{self._spell_name} Get Components: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Components: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'components')

        try:
            components_title = self._tag.find('b', text='Components')

            siblings = components_title.find_next_siblings(string=re.compile("."))

            components_string = siblings[0]

            components = components_string.split(',')
            components = [component.strip() for component in components]

            logger.info(f'{self._spell_name} Get Components: Values are {components}.')

            return components
        except Exception as ex:
            logger.exception(f'Get Components: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'casting_time')

    def get_casting_range(self):
        logger.debug(f'{self._spell_name} Get Casting Range: Ready.')

        if self._tag is None:
            logger.error('Get Casting Range: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'casting_range')

        try:
            casting_range_title = self._tag.find('b', text='Range')

            siblings = casting_range_title.find_next_siblings(string=re.compile("."))

            casting_range = siblings[0]
            casting_range = casting_range.strip().capitalize()

            logger.info(f'Get Casting Range: Value is {casting_range}.')

            return casting_range
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Casting Range: '
                             f'An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'casting_range')

    def get_target(self):
        logger.debug(f'{self._spell_name} Get Target: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Target: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'target')

        try:
            target_title = self._tag.find('b', text='Target')

            siblings = target_title.find_next_siblings(string=re.compile("."))

            target = siblings[0]
            target = target.strip().capitalize()

            logger.info(f'Get Target: Value is {target}.')

            return target
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Target: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'target')

    def get_duration(self):
        logger.debug(f'{self._spell_name} Get Duration: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Duration: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'duration')

        try:
            duration_title = self._tag.find('b', text='Duration')

            siblings = duration_title.find_next_siblings(string=re.compile("."))

            duration = siblings[0]
            duration = duration.strip().capitalize()

            logger.info(f'Get Duration: Value is {duration}.')

            return duration
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Duration: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'duration')

    def get_save(self):
        logger.debug(f'{self._spell_name} Get Save: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Save: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'save')

        try:
            try:
                save_title = self._tag.find('b', text='Saving Throw')

                siblings = save_title.find_next_siblings(string=re.compile("."))

                save = siblings[0]
                save = save.strip().capitalize().replace(';', '')
            except (IndexError, AttributeError):
                logger.debug(f'{self._spell_name} Get Save: Value not found but is optional. Set it to empty')
                save = 'None'

            logger.info(f'{self._spell_name} Get Save: Value is {save}.')

            return save
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Save: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'save')

    def get_spell_resistance(self):
        logger.debug(f'{self._spell_name} Get Spell Resistance: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Spell Resistance: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'spell_resistance')

        try:
            try:
                spell_resistance_title = self._tag.find('b', text='Spell Resistance')

                siblings = spell_resistance_title.find_next_siblings(string=re.compile("."))

                spell_resistance = siblings[0]
                spell_resistance = spell_resistance.strip().capitalize()
            except (AttributeError, IndexError):
                logger.debug(f'{self._spell_name} Get Spell Resistance: Value not found but is optional. '
                             f'Set it to empty')
                spell_resistance = 'No'

            logger.info(f'{self._spell_name} Get Spell Resistance: Value is {spell_resistance}.')

            return spell_resistance
        except Exception as ex:
            logger.exception(f'Get Save: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'spell_resistance')

    def get_description(self):
        logger.debug(f'{self._spell_name} Get Description: Ready.')

        if self._tag is None:
            logger.error(f'{self._spell_name} Get Description: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self._spell_name, 'description')

        try:
            description_title = self._tag.find('h3', class_='framing', text='Description')

            # Descriptions are made with sub elements, line breaks and so on and so forth, so there are multiple texts.
            sibling = description_title.next_sibling
            description_list = []
            while sibling:
                if sibling.text:
                    description_list.append(sibling.text)
                # Add line breaks to keep the description beautiful.
                elif sibling.name == 'br':
                    description_list.append('\n')
                sibling = sibling.next_sibling

            description = ''.join(description_list)
            description = description.strip()

            logger.info(f'{self._spell_name} Get Description: Value is "{description}".')

            return description
        except Exception as ex:
            logger.exception(f'{self._spell_name} Get Description: '
                             f'An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self._spell_name, 'description')
