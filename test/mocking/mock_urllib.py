import logging


class MockUrllibHTTPResponse:
    def __init__(self, text: str):
        self._text = text

    def read(self) -> bytes:
        return self._text.encode('utf8')


class MockUrllibRequestResponse:
    def __init__(self, html_text: str):
        self._html_text = html_text

    def urlopen(self, url) -> MockUrllibHTTPResponse:
        logging.debug(f'Mocking call to address "{url}"')

        return MockUrllibHTTPResponse(self._html_text)


def mock_urllib_request_response_wrapper(html_path) -> MockUrllibRequestResponse:
    from definitions import ROOT_DIR

    with open(ROOT_DIR + html_path, 'r') as file:
        html_text = file.read()
        return MockUrllibRequestResponse(html_text)
