from page_analyzer.connection import connect_db

# информация для заполнение странички urls - дата проверки и статус-код


def c_insert():
    result_list = []
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT MAX(id) FROM urls;"
    )
    data = cur.fetchall()
    id = data[0][0]
    for i in range(1, id + 1):
        cur.execute(
            """SELECT created_at, status_code
            FROM url_checks WHERE url_id=(%s)
            ORDER BY created_at DESC LIMIT 1;""",
            [i]
        )
        data = cur.fetchall()
        if data == []:
            data = [('', '')]
        result_list.extend(data)
    return result_list


def data_addition(data_left, data_right):
    data = []
    max_len = len(data_left)
    i = 1
    while i <= max_len:
        n = (data_left[i-1][0], data_left[i-1][1],
             data_right[-i][0], data_right[-i][1])
        data.append(n)
        i += 1
    return data


if __name__ == '__main__':
    c_insert()
