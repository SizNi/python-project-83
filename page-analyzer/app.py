from dotenv import load_env
from flask import Flask

load_env()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'
