class SpellsPageCrawlingException(Exception):
    def __init__(self, message='unknown error', spell='unknown spell', field='unknown_field'):
        self.spell = spell
        self.field = field
        self.message = message

        super().__init__(message)
