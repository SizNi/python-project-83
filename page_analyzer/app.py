from dotenv import load_dotenv
from flask import Flask, render_template
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/')
def start():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run()
