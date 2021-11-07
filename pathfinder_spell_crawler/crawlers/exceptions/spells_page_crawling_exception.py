class SpellsPageCrawlingException(Exception):
    def __init__(self, message='unknown error', field='unknown field'):
        self.field = field
        self.message = message

        super().__init__(message)
