import re
from typing import List

from bs4 import BeautifulSoup

from pathfinder_spell_crawler.crawlers.crawler import Crawler


class AonprdSpellPageCrawler(Crawler):
    def __init__(self, url):
        super().__init__(url)

        self.tag = None

    def get_spell_tag(self):
        html_global_text = self._get_html_text()

        soup = BeautifulSoup(html_global_text, 'html.parser')

        # See test/samples/fake_page/aonprd_spell_page.html for a HTML sample.
        self.tag = soup.find(id='main').find('table').tr.td.span

    def get_name(self) -> str:
        name = self.tag.find('h1', class_='title').text

        # Remove any whitespace and line break before and after the name.
        name = name.strip()

        return name

    def get_sources(self) -> List[str]:
        sources = []

        source_title = self.tag.find('b', text='Source')
        source_title_next_siblings = source_title.find_next_siblings()

        for sibling in source_title_next_siblings:
            if str(sibling) == '<br/>':
                break
            if sibling.name == 'a':
                source = sibling.text
                source = source.strip()
                sources.append(source)

        return sources

    def get_school(self):
        school_title = self.tag.find('b', text='School')
        siblings = school_title.find_next_siblings()

        # Normally there is always at least one sibling: the main school.
        school = siblings[0].find('a').text
        school = school.strip().capitalize()

        return school

    def get_sub_school(self):
        school_title = self.tag.find('b', text='School')
        siblings = school_title.find_next_siblings()

        # Sub school is optional.
        try:
            sub_school = siblings[1].find('a').text
            sub_school = sub_school.strip().capitalize()
        except IndexError:
            sub_school = ''

        return sub_school

    def get_descriptor(self):
        school_title = self.tag.find('b', text='School')
        siblings = school_title.find_next_siblings()

        # Descriptor is optional.
        try:
            descriptor = siblings[2].find('a').text
            descriptor = descriptor.strip().capitalize()
        except IndexError:
            descriptor = ''

        return descriptor

    def get_levels(self):
        levels_title = self.tag.find('b', text='Level')

        # By default, BeautifulSoup only works with named elements (such as <a>), not simple text.
        # This can be changed using string argument, with a regex containing all possible strings.
        siblings = levels_title.find_next_siblings(string=re.compile("."))

        levels_string = siblings[0]

        levels = levels_string.split(',')
        levels = [level.strip().capitalize() for level in levels]

        return levels

    def get_casting_time(self):
        casting_time_title = self.tag.find('b', text='Casting Time')

        siblings = casting_time_title.find_next_siblings(string=re.compile("."))

        casting_time = siblings[0]
        casting_time = casting_time.strip().capitalize()

        return casting_time

    def get_components(self):
        components_title = self.tag.find('b', text='Components')

        siblings = components_title.find_next_siblings(string=re.compile("."))

        components_string = siblings[0]

        components = components_string.split(',')
        components = [component.strip().upper() for component in components]

        return components

    def get_casting_range(self):
        range_time_title = self.tag.find('b', text='Range')

        siblings = range_time_title.find_next_siblings(string=re.compile("."))

        range_time = siblings[0]
        range_time = range_time.strip().capitalize()

        return range_time

    def get_target(self):
        target_title = self.tag.find('b', text='Target')

        siblings = target_title.find_next_siblings(string=re.compile("."))

        target = siblings[0]
        target = target.strip().capitalize()

        return target

    def get_duration(self):
        duration_title = self.tag.find('b', text='Duration')

        siblings = duration_title.find_next_siblings(string=re.compile("."))

        duration = siblings[0]
        duration = duration.strip().capitalize()

        return duration

    def get_save(self):
        save_title = self.tag.find('b', text='Saving Throw')

        siblings = save_title.find_next_siblings(string=re.compile("."))

        save = siblings[0]
        save = save.strip().capitalize().replace(';', '')

        return save

    def get_spell_resistance(self):
        spell_resistance_title = self.tag.find('b', text='Spell Resistance')

        siblings = spell_resistance_title.find_next_siblings(string=re.compile("."))

        spell_resistance = siblings[0]
        spell_resistance = spell_resistance.strip().capitalize()

        return spell_resistance

    def get_description(self):
        description_title = self.tag.find('h3', class_='framing', text='Description')

        # Descriptions are made with sub elements, line breaks and so on and so forth, so there are multiple texts.
        sibling = description_title.next_sibling
        description_list = []
        while sibling:
            description_list.append(sibling.text)
            sibling = sibling.next_sibling

        description = ''.join(description_list)
        description = description.strip()

        return description
