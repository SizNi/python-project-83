from dotenv import load_dotenv
from flask import Flask, render_template, request
import os
import jinja2
from connection import connect_db
from url_validator import url_val

def id_urls(id):
    print(id)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id=(%s);", [id])
    data = cur.fetchall()
    print(type(data))
    print(data[0][1])
    print(f'{data}\nRead db succesfully')
 

id = 49
id_urls(id) 