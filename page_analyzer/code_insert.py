from page_analyzer.connection import connect_db
import datetime

# информация для заполнение странички urls - дата проверки и статус-код
def c_insert():
    result_list =[]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT MAX(id) FROM urls;"
    )
    data = cur.fetchall()
    id = data[0][0]
    for i in range(1, id + 1):
        cur.execute(
            "SELECT created_at, status_code FROM url_checks WHERE url_id=(%s) ORDER BY created_at DESC LIMIT 1;", [i]
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
        n = (data_left[i-1][0], data_left[i-1][1],data_right[-i][0], data_right[-i][1])
        data.append(n)
        i += 1
    return data

#data_right = [(datetime.datetime(2022, 12, 23, 2, 38, 16, 938049), 200), (datetime.datetime(2022, 12, 23, 2, 38, 34, 710972), 200), (0, 0), (datetime.datetime(2022, 12, 23, 3, 15, 51, 441368), 200), (0, 0)]
#data_left = [(5, 'https://turup.ru'), (4, 'https://kokolo.com'), (3, 'https://koko.com'), (2, 'https://hexlet.io'), (1, 'https://ya.ru')]

#data_addition(data_left, data_right)
    
if __name__ == '__main__':
    c_insert()

