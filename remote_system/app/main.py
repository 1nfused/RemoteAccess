from flask import Flask, render_template, \
    request, url_for, redirect, session, flash, g

from flask.ext.sqlalchemy import SQLAlchemy
import os
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
import json
import logging
import requests
from requests.exceptions import HTTPError, ConnectionError

import constants

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# User class
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, default="root")
    role = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


# Red Pitaya instance class
class RedPitaya(db.Model):
    __tablename__ = "redpitaya"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mac = db.Column(db.String, nullable=False)

    def __init__(self, name, mac):
        self.name = name
        self.mac = mac


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
                # Sesion
                rp = { 'connected': False }
                session['rp'] = rp
                session['logged_in'] = True
                session['logged_user'] = user.username
                return redirect(url_for('index', user=user))
        except AttributeError:
            error = 'You shall not pass'

    return render_template('login.html', error=error)


@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    return

@app.route('/gpio', methods=['GET'])
def gpio():
    return render_template('io_pins.html')


@app.route('/registers', methods=['POST', 'GET'])
def registers():
    return render_template('registers.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# One of the main functions
@app.route('/connect_pitaya', methods=['POST'])
def connect_pitaya():

    rp = request.form.get('button_pitaya', type=str)
    mac = constants.registred_red_pitaya.get(rp)

    # Try and connect to the redpitaya
    try:
        r = requests.get("http://www.ip-address.com")  
    except ConnectionError:
        flash("Could not connect Red Pitaya. Please check your connection")
        return render_template(
            'index.html',
            error="error")
    flash("Successfully connected %s with MAC: %s" % (rp, mac)) 
    return redirect(url_for('index'))


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    response = {"success": True }
    # If we want to update our contant info
    print("Here we are")
    print(request.form.get("add_user", type=str))
    print(request.form.get("add_pitaya", type=str))
    
    if request.method == 'POST':
        username = request.form.get('username', type=str)
        if User.query.filter(username == username).first():
            response = {
                "success": False, "error": "Username already exists"}
            return redirect(url_for('settings', response=response))

        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        email = request.form.get('email', type=str)

        user = User(username, "root", name, email)
        db.session.add(user)
        db.session.commit()
        response = {"success": True, "error": "Successfully created user" }
        return redirect(url_for('settings', response=response))

    return render_template('settings.html', response=response)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    return redirect(url_for('/'))


@app.before_request
def before_request():
        try:
            if session.get('logged_in'):
                g.user = session.get('logged_user')
        except AttributeError:
            return None

if __name__ == '__main__':
    # Global jinja functions
    app.jinja_env.globals.update(connect_pitaya=connect_pitaya)
    app.run()
