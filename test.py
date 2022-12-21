import validators
from urllib.parse import urlparse
from page_analyzer.connection import connect_db

def test(id):
    # будем проверять на наличие в базе
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT created_at FROM url_checks WHERE url_id=(%s) ORDER BY created_at DESC NULLS LAST LIMIT 1;", [id])
    data_checks = cur.fetchall()
    print(str(data_checks[0][0])[:10])

id = 49
test(id)