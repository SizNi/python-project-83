import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL)
    print('db connect')
    return conn


if __name__ == '__main__':
    connect_db()
