from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for
import os
import jinja2
import datetime
from page_analyzer.connection import connect_db
from page_analyzer.url_validator import url_val


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/')
def start():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'main_page.html',
        messages=messages
    )


@app.route('/urls', methods=['GET', 'POST'])
def save_data():
    if request.method == 'POST':
        url = request.form.get('url')
        dt_now = str(datetime.datetime.now())
        print(url)
        # отправляем на проверку
        url = url_val(url)
        # ошибка в случае невведенного адреса
        if url == 'error none':
            flash("URL can't be empty!", 'error')
            return redirect('/')
        # ошибка на False от валидатора
        elif url == 'error format':
            flash("Wrong format of URL!", 'error')
            return redirect('/')
        # ошибка в базе такой урл уже есть
        elif url[0] == 'error, in base':
            flash("Already in base", 'error')
            id = url[1]
            print(id)
            return redirect(
                url_for('id_urls', id=id)
            )
        elif url is not False:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO urls (name, created_at) VALUES (%s,%s);""", (url, dt_now))
            conn.commit()
            print('Insert into db successfully')
            cur.execute(
                "SELECT * FROM urls ORDER BY created_at DESC NULLS LAST;")
            data = cur.fetchall()
            flash('Success', 'sucess')
            return render_template(
                'urls.html',
                data=data
            )
        else:
            return render_template(
                'main_page.html',
                data=data
            )
    else:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls ORDER BY created_at DESC NULLS LAST;")
        data = cur.fetchall()
        return render_template(
            'urls.html',
            data=data
        )


@app.route('/urls/<id>')
def id_urls(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id=(%s);", [id])
    data = cur.fetchall()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'id_urls.html',
        data=data,
        messages=messages
    )


@app.route('/urls/<id>/checks', methods=['GET', 'POST'])
def url_check(id):
    # подключаемся к базе urls
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, created_at FROM urls WHERE id=(%s);", [id])
    data = cur.fetchall()
    # добавляем время последней проверки
    cur.execute("SELECT created_at FROM url_checks WHERE url_id=(%s) ORDER BY created_at DESC NULLS LAST LIMIT 1;", [id])
    data_time = cur.fetchall()
    if data_time != []:
        time = str(data_time[0][0])[:10]
    else:
        time = ''
    # достаем старые проверки
    cur.execute("SELECT * FROM url_checks WHERE url_id=(%s);", [id])
    data_checks = cur.fetchall()
    # messages = get_flashed_messages(with_categories=True)
    # если дата не пустая и гет
    if request.method == 'GET' and data_checks != []:
        return render_template(
            'url_check.html',
            id=id,
            url=data[0][0],
            time=time,
            data_checks=data_checks
        )
    elif request.method == 'GET' and data_checks == []:
        return render_template(
            'url_check.html',
            id=id,
            url=data[0][0],
            time=time
        )
    elif request.method == 'POST':
        # вставляем проверку (пока липовую)
        dt_now = str(datetime.datetime.now())
        cur.execute(
            """INSERT INTO url_checks (url_id, status_code, created_at) VALUES (%s,%s,%s);""", (id, 200, dt_now)
            )
        conn.commit()
        print('Insert into db Cheks successfully')
        flash('Success', 'sucess')
        return redirect(
            url_for('url_check', id=id)
            )
        

if __name__ == '__main__':
    app.run()
