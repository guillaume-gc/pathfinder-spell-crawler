import re
from typing import List

from bs4 import BeautifulSoup

from definitions import WHITELIST
from pathfinder_spell_crawler.crawlers.crawler import Crawler
from pathfinder_spell_crawler.crawlers.exceptions.spells_page_crawling_exception import SpellsPageCrawlingException
from pathfinder_spell_crawler.crawlers.spells.page import logger
from pathfinder_spell_crawler.soup.spell_tags import AonPrdSpellTags


class AonprdSpellPageCrawler(Crawler):
    def __init__(self, spell_name, url):
        super().__init__(url)

        self._tag = None
        self.spell_name = spell_name

    def update_spell_tag(self):
        self._tag = None

        logger.info(f'Update {self.spell_name} Spell Tag: URL is "{self._url}"')

        html_global_text = self._get_html_text()
        logger.info(f'Update {self.spell_name} Spell Tag: HTML extracted.')
        logger.debug(html_global_text)

        logger.info(f'Update {self.spell_name} Spell Tag: Attempt to fix HTML.')
        html_global_text = self._fix_html(html_global_text)
        logger.debug(html_global_text)

        soup = BeautifulSoup(html_global_text, 'html.parser')
        logger.info(f'Update {self.spell_name} Spell Tag: Soup created from HTML.')

        # See test/samples/fake_page/aonprd_spell_page_*.html for HTML samples.
        td_result_set = soup.find_all('td')

        logger.info(f'Update {self.spell_name} Spell Tag: {len(td_result_set)} field found.')

        for tag in td_result_set:
            try:
                # For some reasons, there can be multiple spells inside a single TD element...
                # A solution is to create custom tags, which can only contain one spell.
                spell_soup = AonPrdSpellTags(soup, tag.span, self.spell_name)
                self._tag = spell_soup.create_spell_tag()

                # If spell's tag found, break.
                if self._tag is not None:
                    break
            # If an error related to a missing HTML field happens, ignore it.
            except AttributeError as ex:
                logger.debug(f'Update {self.spell_name} Spell Tag: {type(ex).__name__} -> {ex}.')
                pass

        logger.debug(self._tag)

        if self._tag is None:
            logger.error(f'Update {self.spell_name} Spell Tag: Could not find spell.')
            raise SpellsPageCrawlingException('spell not found', self.spell_name)

    @staticmethod
    def _fix_html(html_global_text):
        # Some HTML <table> tags are broken, fix them
        fixed_html_global_text = re.sub(r'<table[\n.\s*]*class="inner"[\n.\s*]*\)', '<table>', html_global_text)

        return fixed_html_global_text

    def get_name(self) -> str:
        """
        Get name from Crawler. Even though the name is already know, this makes sure the right spell is being worked on.
        :return: Spell name
        """
        logger.debug(f'{self.spell_name} Get Name: Ready.')

        if self._tag is None:
            logger.error('Get Name: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'name')

        try:
            try:
                name = self._tag.find('h1', class_='title').text

                # Remove any whitespace and line break before and after the name.
                name = name.strip()
            except (IndexError, AttributeError):
                logger.exception(f'{self.spell_name} Get Name: No name found.')

                raise SpellsPageCrawlingException(f'no name found', self.spell_name, 'name')

            logger.info(f'Get Name: Name is "{name}".')

            # Remove as many as "non important" differences possible (white spaces, case, etc...)
            if name.lower().replace(' ', '') != self.spell_name.lower().replace(' ', ''):
                logger.error(f'{self.spell_name} Get Name: Name "{name}" does not correspond to "{self.spell_name}".')
                raise SpellsPageCrawlingException('name is not correct', self.spell_name, 'name')

            return name
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Name: Fatal Error.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'name') from ex

    def get_sources(self) -> List[str]:
        logger.debug(f'{self.spell_name} Get Sources: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Sources: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'sources')

        try:
            sources = []

            try:
                source_title = self._tag.find('b', text='Source')
                source_title_next_siblings = source_title.find_next_siblings()

                for sibling in source_title_next_siblings:
                    if str(sibling) == '<br/>':
                        break
                    if sibling.name == 'a':
                        source = sibling.text
                        source = source.strip()
                        sources.append(source)
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Sources: Minor Error {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Sources: No source found.')

            if sources is None:
                sources = []

            logger.info(f'{self.spell_name} Get Sources: Sources are "{sources}".')

            return sources
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Sources: Fatal Error ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'sources') from ex

    def get_school(self):
        logger.debug(f'{self.spell_name} Get School: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Sources: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'school')

        try:
            try:
                school_title = self._tag.find('b', text='School')
                siblings = school_title.find_next_siblings()

                # Normally there is always at least one sibling: the main school.
                school = siblings[0].find('a').text
                school = school.strip()
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get School: Warning {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get School: No school found.')
                school = ''

            if school is None:
                school = ''

            logger.info(f'{self.spell_name} Get School: School is "{school}".')

            return school
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get School: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'An {ex} error occurred', self.spell_name, 'school') from ex

    def get_sub_school(self):
        logger.debug(f'{self.spell_name} Get Sub School: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Sub School: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'sub_school')

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
                        sub_school = text
                        break
                        # Check other possible fields values to see if it's an unknown value
                    if text not in WHITELIST['descriptors'] and text not in WHITELIST['schools']:
                        logger.warning(f'{self.spell_name} Get Sub School: Unknown value found "{text}"')
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Sub School: '
                             f'Optional value not found {type(ex).__name__} -> {ex}.')

            if sub_school is None:
                sub_school = ''

            logger.info(f'{self.spell_name} Get Sub School: Sub School is "{sub_school}".')

            return sub_school
        except Exception as ex:
            logger.exception(f'Get Sub School: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'sub_school') from ex

    def get_descriptors(self) -> List[str]:
        logger.debug(f'{self.spell_name} Get Descriptor: Ready.')

        if self._tag is None:
            logger.error('Get Descriptors: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'descriptor')

        try:
            # Descriptor part of school and is optional.
            school_title = self._tag.find('b', text='School')
            siblings = school_title.find_next_siblings()
            descriptors = []

            try:
                for sibling in siblings:
                    text = sibling.find('a').text.strip()

                    if text == '':
                        continue

                    descriptors += self._find_valid_descriptors(text)
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Descriptors: '
                             f'Optional value not found {type(ex).__name__} -> {ex}.')

            if descriptors is None:
                descriptors = []

            logger.info(f'{self.spell_name} Get Descriptors: Descriptors are "{descriptors}".')

            return descriptors
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Descriptors: Fatal Error ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'descriptors') from ex

    def _find_valid_descriptors(self, text) -> List[str]:
        text_elements = text.split(',')
        descriptors = []
        for e in text_elements:
            if e in WHITELIST['descriptors']:
                descriptor = e.strip()
                descriptors.append(descriptor)
            # Check other possible fields values to see if it's an unknown value
            elif e not in WHITELIST['sub_schools'] and text not in WHITELIST['schools']:
                logger.warning(f'{self.spell_name} Get Descriptors: Unknown value found, is "{text}".')

        return descriptors

    def get_levels(self) -> List[str]:
        logger.debug('Get Levels: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Levels: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'levels')

        try:
            try:
                levels_title = self._tag.find('b', text='Level')

                # By default, BeautifulSoup only works with named elements (such as <a>), not simple text.
                # This can be changed using string argument, with a regex containing all possible strings.
                siblings = levels_title.find_next_siblings(string=re.compile("."))

                levels_string = siblings[0]

                levels = levels_string.split(',')
                levels = [level.strip() for level in levels]
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Levels: '
                             f'Optional value not found {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Levels: No level found.')
                levels = []

            if levels is None:
                levels = []

            logger.info(f'{self.spell_name} Get Levels: Levels are "{levels}".')

            return levels

        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Levels: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'levels') from ex

    def get_casting_time(self):
        logger.debug(f'{self.spell_name} Get Casting Time: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Casting Time: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'casting_time')

        try:
            try:
                casting_time_title = self._tag.find('b', text='Casting Time')

                siblings = casting_time_title.find_next_siblings(string=re.compile("."))

                casting_time = siblings[0].strip()
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Casting Time: Warning {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Casting Time: No casting time found.')
                casting_time = ''

            if casting_time is None:
                casting_time = ''

            logger.info(f'{self.spell_name} Get Casting Time: Casting time is "{casting_time}".')

            return casting_time
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Casting Time: Fatal Error ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'casting_time') from ex

    def get_components(self):
        logger.debug(f'{self.spell_name} Get Components: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Components: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'components')

        try:
            try:
                components_title = self._tag.find('b', text='Components')

                siblings = components_title.find_next_siblings(string=re.compile("."))

                components_string = siblings[0]

                components = components_string.split(',')
                components = [component.strip() for component in components]
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Components: Fatal Error {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Components: No components found.')
                components = []

            if components is None:
                components = []

            logger.info(f'{self.spell_name} Get Components: Components are "{components}".')

            return components
        except Exception as ex:
            logger.exception(f'Get Components: an exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'casting_time') from ex

    def get_casting_range(self):
        logger.debug(f'{self.spell_name} Get Casting Range: Ready.')

        if self._tag is None:
            logger.error('Get Casting Range: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'casting_range')

        try:
            try:
                casting_range_title = self._tag.find('b', text='Range')

                siblings = casting_range_title.find_next_siblings(string=re.compile("."))

                casting_range = siblings[0].strip()
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Casting Range: Warning {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Casting Range: No casting range found.')
                casting_range = ''

            if casting_range is None:
                casting_range = ''

            logger.info(f'{self.spell_name} Get Casting Range: Casting rage is "{casting_range}".')

            return casting_range
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Casting Range: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'casting_range') from ex

    def get_target(self):
        logger.debug(f'{self.spell_name} Get Target: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Target: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'target')

        try:
            target_possible_fields = ['Target', 'Targets']
            target = None
            for field in target_possible_fields:
                try:
                    target_title = self._tag.find('b', text=field)

                    siblings = target_title.find_next_siblings(string=re.compile("."))

                    target = siblings[0]
                    target = target.strip()

                    logger.info(f'{self.spell_name} Get Target: Field is "{field}" and target is "{target}".')

                    break
                except (AttributeError, IndexError) as ex:
                    logger.debug(f'{self.spell_name} Get Target: Warning for {field} {type(ex).__name__} -> {ex}. '
                                 f'Attempt another field.')

            if target is None:
                target = ''

            logger.info(f'{self.spell_name} Get Target: Target is "{target}".')

            return target
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Target: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'target') from ex

    def get_area(self):
        logger.debug(f'{self.spell_name} Get Area: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Area: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'duration')

        try:
            try:
                area_title = self._tag.find('b', text='Area')

                siblings = area_title.find_next_siblings(string=re.compile("."))

                area = siblings[0].strip()
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Area: Optional Value not found {type(ex).__name__} -> {ex}.')
                area = ''

            if area is None:
                area = ''

            logger.info(f'{self.spell_name} Get Area: Area is "{area}".')

            return area
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Area: Fatal Error {ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'area') from ex

    def get_effect(self):
        logger.debug(f'{self.spell_name} Get Effect: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Effect: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'duration')

        try:
            try:
                effect_title = self._tag.find('b', text='Effect')

                siblings = effect_title.find_next_siblings(string=re.compile("."))

                effect = siblings[0].strip()
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Effect: Optional Value not found {type(ex).__name__} -> {ex}.')
                effect = ''

            if effect is None:
                effect = ''

            logger.info(f'{self.spell_name} Get Effect: Effect is "{effect}".')

            return effect
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Effect: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'effect') from ex

    def get_duration(self):
        logger.debug(f'{self.spell_name} Get Duration: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Duration: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'duration')

        try:
            try:
                duration_title = self._tag.find('b', text='Duration')

                siblings = duration_title.find_next_siblings(string=re.compile("."))

                duration = siblings[0].strip()

            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Duration: Warning {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Duration: No duration found.')
                duration = ''

            if duration is None:
                duration = ''

            logger.info(f'Get Duration: Duration is "{duration}".')

            return duration
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Duration: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'duration') from ex

    def get_save(self):
        logger.debug(f'{self.spell_name} Get Save: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Save: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'save')

        try:
            try:
                save_title = self._tag.find('b', text='Saving Throw')

                siblings = save_title.find_next_siblings(string=re.compile("."))

                save = siblings[0]
                save = save.strip().replace(';', '')
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Save: '
                             f'Optional Value not found {type(ex).__name__} -> {ex}.')
                save = 'none'

            if save is None:
                save = 'none'

            logger.info(f'{self.spell_name} Get Save: Save is "{save}".')

            return save
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Save: An exception occurred ({ex} -> {type(ex).__name__}).')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'save') from ex

    def get_spell_resistance(self):
        logger.debug(f'{self.spell_name} Get Spell Resistance: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Spell Resistance: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'spell_resistance')

        try:
            try:
                spell_resistance_title = self._tag.find('b', text='Spell Resistance')

                siblings = spell_resistance_title.find_next_siblings(string=re.compile("."))

                spell_resistance = siblings[0]
                spell_resistance = spell_resistance.strip()
            except (AttributeError, IndexError) as ex:
                logger.debug(f'{self.spell_name} Get Spell Resistance: '
                             f'Optional Value not found {type(ex).__name__} -> {ex}.')
                spell_resistance = 'no'

            if spell_resistance is None:
                spell_resistance = 'no'

            logger.info(f'{self.spell_name} Get Spell Resistance: Spell Resistance is "{spell_resistance}".')

            return spell_resistance
        except Exception as ex:
            logger.exception(f'Get Save: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'spell_resistance') from ex

    def get_description(self) -> str:
        logger.debug(f'{self.spell_name} Get Description: Ready.')

        if self._tag is None:
            logger.error(f'{self.spell_name} Get Description: Tag is not initialized. Call get_spell_tag method.')
            raise SpellsPageCrawlingException('tag not initialized', self.spell_name, 'description')

        try:
            try:
                description_title = self._tag.find('h3', class_='framing', text='Description')

                # Descriptions are made with sub elements, line breaks and so on and so forth,
                #   so there are multiple texts.
                sibling = description_title.next_sibling
                description_list = []
                while sibling:
                    # h1, h2... tags are not within the description
                    if sibling.name is not None and sibling.name.startswith('h'):
                        break

                    if sibling.text:
                        description_list.append(sibling.text)
                    # Add line breaks to keep the description beautiful.
                    elif sibling.name == 'br':
                        description_list.append('\n')

                    sibling = sibling.next_sibling

                description = ''.join(description_list)
                description = description.strip()
            except (IndexError, AttributeError) as ex:
                logger.debug(f'{self.spell_name} Get Description: Warning {type(ex).__name__} -> {ex}.')
                logger.warning(f'{self.spell_name} Get Description: No description found.')
                description = ''

            if description is None:
                description = ''

            logger.info(f'{self.spell_name} Get Description: Value is "{description}".')

            return description
        except Exception as ex:
            logger.exception(f'{self.spell_name} Get Description: Fatal Error {ex} -> {type(ex).__name__}.')
            raise SpellsPageCrawlingException(f'an {ex} error occurred', self.spell_name, 'description') from ex
