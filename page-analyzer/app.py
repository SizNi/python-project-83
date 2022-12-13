from dotenv import load_dotenv
from flask import Flask
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'

if __name__ == '__main__':
    app.run()
