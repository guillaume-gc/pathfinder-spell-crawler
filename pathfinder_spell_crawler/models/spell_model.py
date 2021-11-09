from pathfinder_spell_crawler.crawlers.spells.page.aonprd_spells_page_crawler import AonprdSpellPageCrawler


class SpellModel:
    def __init__(self):
        self.name = None
        self.source = None

        self.school = None
        self.sub_school = None
        self.descriptors = None

        self.levels = None

        self.casting_time = None

        self.components = None

        self.casting_range = None

        self.target = None
        self.effect = None
        self.area = None
        self.duration = None
        self.save = None
        self.spell_resistance = None

        self.description = None

    def set_data_from_page_crawler(self, page_crawler: AonprdSpellPageCrawler):
        self.name = page_crawler.get_name()
        self.source = page_crawler.get_sources()
        self.school = page_crawler.get_school()
        self.sub_school = page_crawler.get_sub_school()
        self.descriptors = page_crawler.get_descriptors()
        self.levels = page_crawler.get_levels()
        self.casting_time = page_crawler.get_casting_time()
        self.components = page_crawler.get_components()
        self.target = page_crawler.get_target()
        self.effect = page_crawler.get_effect()
        self.effect = page_crawler.get_area()
        self.duration = page_crawler.get_duration()
        self.save = page_crawler.get_save()
        self.spell_resistance = page_crawler.get_spell_resistance()
        self.description = page_crawler.get_description()
