from dotenv import load_dotenv
from flask import Flask, render_template, request
import os
import jinja2
from connection import connect_db
from url_validator import url_val


def id_urls():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT url_id FROM url_checks;"
    )
    data = cur.fetchall()
    max_numbers = data
    print(max_numbers)
    cur.execute(
        "SELECT url_id, created_at, status_code FROM url_checks;"
    )
    data_checks = cur.fetchall()
    print(len(data_checks))
    print(data_checks[0])


id_urls()
