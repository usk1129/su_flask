#!/usr/bin/env python3
from flask import render_template, request, url_for
from app import app
from app import db
import sqlite3
import yaml


config_file = 'config.yaml'
with open(config_file,'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

@app.route('/')
@app.route('/submit', methods=['GET','POST'])
def bacon_form():
    if request.method == "POST":
       long  = request.form.get('long')
       short = request.form.get('short')
       sms = request.form.get('sms')
       rubrik = request.form.get('rubrik')
       username = request.form.get('username')
       twitter = request.form.get('twitter')
       conn = sqlite3.connect(cfg['database_path'])
       cur = conn.cursor()
       cur.execute("INSERT INTO driftinfo (rubrik,big,small,sms,username)  VALUES(?,?,?,?,?)",(rubrik,long,short,sms,username))
       conn.commit()
       cur.close()
       return   render_template('/submit.html',rubrik=rubrik,long=long,short=short,sms=sms,username=username)
    return render_template('/base.html', title='Home')


app.secret_key='secret123'



