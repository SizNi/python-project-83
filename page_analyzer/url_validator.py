import validators
from urllib.parse import urlparse


def url_val(url):
    if url is not None:
        # добавляем https если его нет
        url = normalize_ur(url)
        if validators.url(url):
            o = urlparse(url)
            # возращаем нормализованный юрл
            return f'{o.scheme}://{o.netloc}'
    else:
        return False


def normalize_ur(url):
    if url[:5] == 'https':
        return url
    elif url[:5] == 'http:':
        return f'https{url[4:]}'
    return f'https://{url}'

