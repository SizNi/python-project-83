from dotenv import load_dotenv
from flask import (
    Flask, render_template,
    request, flash,
    redirect, get_flashed_messages,
    url_for
)
import os
import datetime
from page_analyzer.connection import connect_db
from page_analyzer.url_validator import url_val
from page_analyzer.request_url import req_url
from page_analyzer.find_tags import tags_check
from page_analyzer.code_insert import c_insert, data_addition


load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.secret_key = SECRET_KEY

@app.route('/')
def start():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'main_page.html',
        messages=messages
    )


@app.route('/urls', methods=['GET', 'POST'])
def save_data():
    # получаем правые два столбца
    if request.method == 'POST':
        data = []
        url = request.form.get('url')
        dt_now = str(datetime.datetime.now())
        # отправляем на проверку
        url = url_val(url)
        # ошибка в случае невведенного адреса
        if url == 'error none':
            flash("URL обязателен", 'danger')
            return redirect('/')
        # ошибка на False от валидатора
        elif url == 'error format':
            flash("Некорректный URL", 'danger')
            return redirect('/')
        # ошибка в базе такой урл уже есть
        elif url[0] == 'error, in base':
            flash("Страница уже существует", 'info')
            id = url[1]
            return redirect(
                url_for('url_check', id=id)
            )
        elif url is not False:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO urls (name, created_at)
                VALUES (%s,%s);""", (url, dt_now)
            )
            conn.commit()
            cur.execute(
                "SELECT id, name FROM urls ORDER BY id DESC NULLS LAST;"
            )
            data_left = cur.fetchall()
            data_right = c_insert()
            data = data_addition(data_left, data_right)
            flash('Cтраница успешно добавлена', 'success')
            return redirect(
                url_for(
                    'url_check',
                    id=data_left[0][0]
                )
            )
        else:
            return render_template(
                'main_page.html',
                data=data
            )
    else:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name FROM urls ORDER BY id DESC;")
        data_left = cur.fetchall()
        data_right = c_insert()
        data = data_addition(data_left, data_right)
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
    cur.execute(
        "SELECT created_at, status_code FROM url_checks WHERE url_id=(%s);", [
            id]
    )
    data_checks = cur.fetchall()
    if data_checks != []:
        time = str(data_checks[-1][0])[:10]
    else:
        time = ''
        data_checks = [('')]
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'id_urls.html',
        data=data,
        messages=messages,
        data_checks=data_checks,
        time=time
    )


@app.route('/urls/<id>/checks', methods=['GET', 'POST'])
def url_check(id):
    # подключаемся к базе urls
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, created_at FROM urls WHERE id=(%s);", [id])
    data = cur.fetchall()
    # добавляем время последней проверки
    cur.execute("SELECT created_at FROM urls WHERE id=(%s);", [id])
    data_time = cur.fetchall()
    if data_time != []:
        time = str(data_time[0][0])[:10]
    else:
        time = ''
    # достаем старые проверки
    cur.execute(
        "SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC;", [id])
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
        # извлекаем url
        cur.execute("SELECT name FROM urls WHERE id=(%s);", [id])
        url = cur.fetchall()
        # отправляем на проверку
        response = req_url(url[0][0])
        # добавляем флеш в зависимости от ответа и вставляем если можем
        if response == 200:
            flash('Страница успешно проверена', 'success')
            # вызываем вторую часть проверки
            h1_tag, title_tag, meta_tag = tags_check(url[0][0])
            # вставляем проверку
            dt_now = str(datetime.datetime.now())
            cur.execute(
                """INSERT INTO url_checks (url_id, status_code,
                h1, title, description, created_at)
                VALUES (%s,%s,%s,%s,%s,%s);""", (
                    id, response, h1_tag, title_tag, meta_tag, dt_now
                )
            )
            conn.commit()
        else:
            flash('Произошла ошибка при проверке', 'danger')
        return redirect(
            url_for('url_check', id=id)
        )


@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
