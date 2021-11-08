from pathfinder_spell_crawler.soup import logger
from pathfinder_spell_crawler.soup.soup import Soup


class SpellTags(Soup):
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

        for sub_tag in self._tags:
            logger.debug(sub_tag)

            current_spell_name = sub_tag.h1.text.strip()
            logger.info(f'Iterate Through Sub Tags: "{current_spell_name}" spell found.')

            if current_spell_name == self._target_spell_name:
                logger.info('Iterate Through Sub Tags: Found target spell.')
                return sub_tag

        logger.warning(f'Iterate Through Sub Tags: Target spell {self._target_spell_name} not found.')

        return None

    def _create_tags(self) -> None:
        logger.info(f'Create Sub Tags: Has {len(self._reference_tag.contents)} content children, '
                    f'target is {self._target_spell_name}.')
        current_sub_tag = None
        self._tags = []

        for content in self._reference_tag.contents:
            logger.debug(content)

            # If H1 tag found or last child (no sibling, attempt to add sub_tag to sub_tags list.
            if content.name == 'h1':
                logger.info('Create Sub Tags: H1 Tag found or no more sibling, consider it as a new spell.')

                self._add_to_tags(current_sub_tag)

                current_sub_tag = self._soup.new_tag('span')

            if current_sub_tag:
                logger.debug(f'Create Sub Tags: Add content to Sub Tag.')
                current_sub_tag.append(content)
            else:
                logger.debug(f'Create Sub Tags: Sub tag is not yet set, no content added.')

        logger.info('Create Sub Tags: all element iterate, add any remaining elements as a spell.')
        self._add_to_tags(current_sub_tag)

    def _add_to_tags(self, current_sub_tag) -> None:
        if current_sub_tag and len(current_sub_tag) > 0:
            logger.info('Add element to Sub Tags: Current Spell Data are not empty, add them to the list of sub tags.')
            self._tags.append(current_sub_tag)
        else:
            logger.info(f'Add element to Sub Tags: Current Spell Data are empty, no content added.')
