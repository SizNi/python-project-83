import validators
from urllib.parse import urlparse
from page_analyzer.connection import connect_db

def test(id):
    # будем проверять на наличие в базе
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM url_checks WHERE url_id=(%s);", [id])
    data_checks = cur.fetchall()
    print(data_checks)

id = 50
test(id)