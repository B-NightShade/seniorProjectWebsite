# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:55:14 2023

@author: weste
"""

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from flask_login import LoginManager, UserMixin, login_user, \
    logout_user, current_user, login_required


app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = "secret"

USER = 'ESSWebsite2023'
PASSWORD = 'ConergyDonation'
HOST = 'ESSWebsite2023.mysql.pythonanywhere-services.com'
DATABASE = 'ESSWebsite2023$EES'


try:
    connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Wrong name/password", flush=True)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist", flush=True)
    else:
        print(err)
else:
    print("connected: connection successfule", flush=True)
    #connection.close()


'''
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    global connection
    cursor = connection.cursor()
    query = "SELECT username FROM user_login WHERE"
    user =
    return user
'''
@app.route('/')
def home():
    a = False
    return render_template("home.html", a=a)


@app.route('/login', methods=['GET','POST'])
def login():
    a = False
    global connection
    if request.method =="POST":
        print("hey")
        username = request.form['username']
        password = request.form['password']
        try:
            cursor = connection.cursor()
            query = "SELECT Pass FROM user_login WHERE Username = %s"
            cursor.execute(query, (username,))
            user=cursor.fetchall()
            cursor.close()
            print("user:")
            print(len(user))
            if len(user) != 0:
                for row in user:
                    userpass = row[0]
                if password == userpass:
                    #login_user(user)
                    return render_template("home.html", a=a)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    return render_template("login.html", a=a)

@app.route("/create")
def create():
    #a = current_user.is_authenticated
    a=False
    return render_template("create.html", a=a)

@app.route("/update")
def update():
    a = False
    return render_template("update.html", a=a)

@app.route("/delete")
def delete():
    a = False
    return render_template("delete.html", a=a)

@app.route("/view")
def view():
    a = False
    return render_template("view.html", a=a)
'''
@app.route('/logout', methods=['GET','POST'])
def logout():
    a = False
    if request.method == "POST":
        logout_user()
    return render_template("logout.html", a=a)
'''
if __name__ == '__main__':
    app.run(port=5050)