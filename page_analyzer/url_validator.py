import validators
from urllib.parse import urlparse
from page_analyzer.connection import connect_db


def url_val(url):
    # проверка на пустое поле
    if url == '':
        return 'error none'
    elif url != '':
        # добавляем https если его нет
        url = normalize_ur(url)
        if validators.url(url):
            o = urlparse(url)
            # возращаем нормализованный юрл
            normalize_url = f'{o.scheme}://{o.netloc}'
            # будем проверять на наличие в базе
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT id,name FROM urls WHERE name = (%s);", [normalize_url])
            data = cur.fetchall()
            # если не нашлось:
            if data == []:
                return normalize_url
            # если нашлось - возвращаем ошибку и id:
            else:
                return ('error, in base', data[0][0])
        else:
            return 'error format'


def normalize_ur(url):
    if url[:5] == 'https':
        return url
    elif url[:5] == 'http:':
        return f'http{url[4:]}'
    return f'https://{url}'
