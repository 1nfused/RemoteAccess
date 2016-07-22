from flask import Flask, render_template, \
    request, url_for, redirect, session, flash, g

from flask.ext.sqlalchemy import SQLAlchemy
import os
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
import json
import logging

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, default="root")
    role = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


@app.route('/', methods=['GET', 'POST'])
def login_page():
    error = None
    # Login authentication
    if request.method == 'POST':
        login_user = request.form.get('data.username', type=str)
        login_password = request.form.get('data.password', type=str)

        print login_user
        print login_password
        user = User.query.filter(
            User.username  == str(login_user)).first()

        try:
            if login_user != user.username or \
                login_password != user.password:
                    error = 'You shall not pass'
            else:
                session['logged_in'] = True
                session['logged_user'] = user.username
                return redirect(url_for('index', user=user))
        except AttributeError:
            error = 'You shall not pass'

    return render_template('login.html', error=error)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', error="error")

if __name__ == '__main__':
    app.run()