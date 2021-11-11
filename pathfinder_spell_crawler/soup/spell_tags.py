from itertools import groupby

from pathfinder_spell_crawler.soup import logger
from pathfinder_spell_crawler.soup.soup import Soup


class AonPrdSpellTags(Soup):
    """
    This class creates a Soup's tag containing exclusively a single spell.
    For some reasons, there can be multiple tags inside a single spell tag in AonPRD...
    """

    def __init__(self, soup, reference_tag, target_spell_name):
        super().__init__(soup)

        self._target_spell_name = target_spell_name
        self._reference_tag = reference_tag

        self._tags = []

    def create_spell_tag(self):
        self._create_tags()

        if self._tags:
            tag = self._tags_search()
        else:
            tag = None

        return tag

    def _tags_search(self):
        logger.info(f'Iterate Through Sub Tags: Target spell is "{self._target_spell_name}".')

        for tag in self._tags:
            logger.debug(tag)

            current_spell_name = tag.h1.text.strip()
            logger.info(f'Iterate Through Sub Tags: "{current_spell_name}" spell found.')

            if current_spell_name == self._target_spell_name:
                logger.info('Iterate Through Sub Tags: Found target spell.')
                return tag

        logger.warning(f'Iterate Through Sub Tags: Target spell {self._target_spell_name} not found.')

        return None

    def _create_tags(self) -> None:
        logger.info(f'Create Sub Tags: Has {len(self._reference_tag.contents)} content children, '
                    f'target is {self._target_spell_name}.')
        self._tags = []

        # All spells start with a H1 element.

        # List with all elements minus their respective H1 element.
        elements_list = [list(group) for k, group in groupby(self._reference_tag, lambda x: x.name == 'h1') if not k]
        # There can be empty elements, or elements unrelated to spells, remove them.
        cleaned_up_elements_list = self._clean_up_elements_list(elements_list)
        # List with all H1 elements.
        split_element_list = [list(group) for k, group in groupby(self._reference_tag, lambda x: x.name == 'h1') if k]
        # Merge the two lists elementwise.
        final_list = [a + b for a, b in zip(split_element_list, cleaned_up_elements_list)]

        # Create new tags based on the final list containing all elements related to a spell.
        for elements in final_list:
            tag = self._soup.new_tag('span')
            tag.extend(elements)

            self._tags.append(tag)

        logger.info(f'Create Sub Tags: {len(self._tags)} spells found.')

    @staticmethod
    def _clean_up_elements_list(elements_list):
        cleaned_up_list = []

        for e in elements_list:
            if AonPrdSpellTags._clean_up_elements_list_checker(e, 'Source'):
                cleaned_up_list.append(e)

        return cleaned_up_list

    @staticmethod
    def _clean_up_elements_list_checker(e, value):
        try:
            return any(x for x in e
                       if hasattr(x, 'contents') and len(x.contents) > 0 and x.contents[0].strip() == value)
        except (AttributeError, IndexError) as ex:
            logger.debug(f'Clean Up Element List Checker: {type(ex)} -> {ex}')
            return False
