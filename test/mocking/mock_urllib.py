import logging


class MockUrllibHTTPResponse:
    def __init__(self, text: str):
        self._text = text

    def read(self) -> bytes:
        return self._text.encode('utf8')


class MockUrllibRequestResponse:
    def __init__(self, html_text: str):
        self._html_text = html_text

    def urlopen(self, url, *args, **kwargs) -> MockUrllibHTTPResponse:
        logging.debug(f'Mocking call to address "{url}"')
        log_args(args, kwargs)

        return MockUrllibHTTPResponse(self._html_text)


def mock_urllib_request_response_wrapper(html_path) -> MockUrllibRequestResponse:
    from definitions import ROOT_DIR

    with open(ROOT_DIR + html_path, 'r', encoding='utf-8') as file:
        html_text = file.read()
        return MockUrllibRequestResponse(html_text)


def log_args(args, kwargs) -> None:
    logging.debug('args')
    logging.debug(args)
    logging.debug('kwargs')
    logging.debug(kwargs)
