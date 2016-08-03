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
import os
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
    role = db.Column(db.Boolean, default=False)

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


# Uses sockets to connect to a scpi server running on a remote device
@app.route('/scpi_server', methods=['GET', 'POST'])
def scpi_server():

    # Scpi args are in form ARG1 ARG2,...,ARGN
    # as defined in scpi-99 standard
    scpi_command = request.form.get('scpi_command')
    scpi_args = request.form.get('scpi_args').split(' ')
    rp = session.rp

    if request.method == 'POST':
        try:
            flash("Successfully executed SCPI command")
        except:


    return render_template('scpi_server.html')


@app.route('/gpio', methods=['GET'])
def gpio():
    return render_template('io_pins.html')


@app.route('/registers', methods=['POST', 'GET'])
def registers():
    return render_template('registers.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    
    # Get all avaliable Red Pitaya
    registred_pitayas = RedPitaya.query.all()
    print registred_pitayas

    return render_template('index.html')


# One of the main functions
@app.route('/connect_pitaya', methods=['POST'])
def connect_pitaya():

    rp_name = request.form.get('button_pitaya', type=str)
    rp_mac = constants.registred_red_pitaya.get(rp_name)
    rp_temp_dir = "/tmp/pitaya1"

    # Try and connect to the redpitaya
    try:
        # TODO: DISCOVER PITAYA
        # TODO: On page load, check avaliability of all pitayas
        rp_ip = "192.168.1.100" # = discover(rp_mac)
        # if not os.path.exists(rp_temp_dir):
        #    os.makedirs(rp_temp_dir)
        response = os.system(
            "echo root | sshfs -o "
            "password_stdin root@192.168.1.100:/ /tmp/pitaya")

        if response == 0:
            session.rp["connected"] = True
    except ConnectionError:
        flash(
            "Could not connect Red Pitaya."
            "Please check your connection")
        return render_template(
            'index.html',
            error="error")
    flash("Successfully connected %s with MAC: %s" % (rp_name, rp_mac)) 
    return redirect(url_for('index'))


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    response = {
        "success": True
    }

    add_type = request.form.get('settings_add')

    if request.method == 'POST' and add_type == 'user':
        username = request.form.get('username', type=str)
        if User.query.filter(User.username == username).first():
            flash("User with username %s already exists" % username)
            return render_template('settings.html', error="error")

        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        email = request.form.get('email', type=str)

        if not name or not surname or not email:
            flash("All fields are required!")
            return render_template('settings.html', error="error")

        # Create user
        user = User(username, "root", name, email)
        db.session.add(user)
        db.session.commit()
        
        # Flash response
        response = { "success": True }
        flash("Successfully created user %s" % (username))
        return redirect(url_for('settings.html', response=response))
    
    elif request.method == 'POST' and add_type == 'pitaya':
        rp_name = \
            request.form.get("rp_name", type=str)
        rp_mac = \
            request.form.get("rp_mac", type=str)

        # Check if MAC is correct right away
        if len(rp_mac) != 12:
            flash("Invalid MAC address!")
            return render_template('settings.html', error="error")

        if not rp_name or not rp_mac:
            flash("All fields are require!")
            return render_template('settings.html', error="error")

        if RedPitaya.query.filter(RedPitaya.mac == rp_mac).first():
            flash("RedPitaya already exists!")
            return render_template('settings.html', error="error")
        else:
            rp = RedPitaya(rp_name, rp_mac)
            db.session.add(rp)
            db.session.commit()

    flash("Successfully created Red Pitaya %s" % rp_name)
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
