from dotenv import load_dotenv
from flask import Flask
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'
