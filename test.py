import validators
from urllib.parse import urlparse
from page_analyzer.connection import connect_db

def test(normalize_url):
    # будем проверять на наличие в базе
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,name FROM urls WHERE name = (%s);", [normalize_url])
    data = cur.fetchall()
    print(data[0][0])

normalize_url = 'https://kokabaoudn.ru'
test(normalize_url)