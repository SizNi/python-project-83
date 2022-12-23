from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for
import os
import jinja2
import datetime
from page_analyzer.connection import connect_db
from page_analyzer.url_validator import url_val
from page_analyzer.request_url import req_url
from page_analyzer.find_tags import tags_check
from page_analyzer.code_insert import c_insert


def test():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name FROM urls ORDER BY id DESC NULLS LAST;")
    data_left = cur.fetchall()
    print(data_left)

test()
