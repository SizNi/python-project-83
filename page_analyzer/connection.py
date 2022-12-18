import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def connect_db():
    DB_NAME = "pproject-83"
    DB_USER = "ovechka"
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = "localhost"
    DB_PORT = "5432"
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS,
                            host=DB_HOST, port=DB_PORT)
    print("Database connected successfully")
    return conn

if __name__ == '__main__':
    connect_db()
