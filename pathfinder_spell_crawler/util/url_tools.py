from urllib.parse import urlparse


def get_domain(url) -> str:
    parse_result = urlparse(url)

    return f'{parse_result.scheme}://{parse_result.netloc}/'
