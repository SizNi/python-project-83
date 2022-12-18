from dotenv import load_dotenv
from flask import Flask, render_template, request
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
    return render_template('main_page.html')


@app.post('/urls')
def save_data():
    url = request.form.get('url')
    dt_now = str(datetime.datetime.now())
    # отправляем на проверку
    url = str(url_val(url))
    if url is not False:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO urls (name, created_at) VALUES (%s,%s);""", (url, dt_now))
        conn.commit()
        print('Insert into db successfully')
        cur.execute("SELECT * FROM urls ORDER BY created_at DESC NULLS LAST;")
        data = cur.fetchall()
        return render_template(
            'urls.html',
            data=data
        )
    else:
        return render_template(
            'main_page.html',
            data=data
        )


@app.route('/urls')
def urls():
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
    return render_template(
        'id_urls.html',
        data=data
    )
    

if __name__ == '__main__':
    app.run()
