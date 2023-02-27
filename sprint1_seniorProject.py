# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:55:14 2023

@author: weste
"""

from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, UserMixin, login_user, \
    #logout_user, current_user, login_required



app = Flask(__name__, static_url_path='/static')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blackjack.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"
#db = SQLAlchemy(app)
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
    app.run()