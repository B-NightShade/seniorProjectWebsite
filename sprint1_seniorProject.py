# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:55:14 2023

@author: weste
"""

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
#from flask_login import LoginManager, UserMixin, login_user, \
    #logout_user, current_user, login_required



app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = "secret"
try:
    connection = mysql.connector.connect(user='ESSWebsite2023', password='ConergyDonation', host='ESSWebsite2023.mysql.pythonanywhere-services.com', database='ESSWebsite2023$EES')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Wrong name/password", flush=True)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist", flush=True)
    else:
        print(err)
else:
    print("connected", flush=True)
    connection.close()

#login_manager = LoginManager(app)
#login_manager.init_app(app)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template("login.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/view")
def view():
    return render_template("view.html")

if __name__ == '__main__':
    app.run(port=5050)