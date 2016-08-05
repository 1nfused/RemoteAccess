
import os
import datetime
import json
import logging
import requests
import urllib2
import subprocess

from flask import Flask, render_template, \
    request, url_for, redirect, session, flash, g

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
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

    def __init__(self, username, password, name, email, group_id):
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

    def __init__(self, name, mac, group_id):
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
                rp = { 
                    'connected': False,
                    'ip': None
                }
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
    scpi_args = request.form.get('scpi_args')
    if scpi_args:
        scpi_args = scpi_args.split(' ')
    
    rp = session['rp']

    if request.method == 'POST':
        try:
            flash("Successfully executed SCPI command")
        except:
            flash("SCPI command failed to execute")
    return render_template('scpi_server.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
        
    avaliable_rp = {}

    # Get all avaliable Red Pitaya in subnet 192.168.1.X
    rp_sweep = \
        subprocess.Popen(
            ['sudo', 'arp-scan', '--interface=wlp3s0', '192.168.1.0/24'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    stdout, stderr = rp_sweep.communicate()

    # Avaliable Red Pitaya are a combination of registred rp and found rp
    # with arp-scan
    for address in stdout.split('\n'):
        split = address.split('\t')
        try:
            if split[2] == constants.RP_HOSTNAME:
                # Get a pitaya with the same mac
                rp = RedPitaya.query.filter(
                    RedPitaya.mac == split[1].upper()).first()
                # Append pitaya to list if any
                if rp:
                    avaliable_rp[split[0]] = rp 
            else:
                continue
        except IndexError:
            continue

    return render_template(
        'index.html', 
        avaliable_rp=avaliable_rp)

@app.route('/logs', methods=['GET', 'POST'])
def logs():
    return render_template('logs.html')

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
        return render_template('settings.html', response=response)
    
    elif request.method == 'POST' and add_type == 'pitaya':
        rp_name = \
            request.form.get("rp_name", type=str)
        rp_mac = \
            request.form.get("rp_mac", type=str)

        # Check if MAC is correct right away
        if len(rp_mac) != 17:
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

# IDEA FOR registers
# When the redpitaya gets mounted, execute a C script or something, that will
# run in the background and constantly pool data from the registers and GPIO

@app.route('/gpio', methods=['GET'])
def gpio():
    # Read GPIO file from mounted RP
    return render_template('io_pins.html')


@app.route('/registers', methods=['POST', 'GET'])
def registers():
    # Read registers file from mounted RP
    return render_template('registers.html')

# One of the main functions
@app.route('/connect_pitaya', methods=['POST'])
def connect_pitaya():

    # When the pitaya gets connected, we have to initiate
    # a bunch of crap. Like scpi server. Like a custom C script
    # that will pull on registers.

    rp_name = request.form.get('button_pitaya', type=str)
    rp_mac = constants.registred_red_pitaya.get(rp_name)
    rp_temp_dir = "/tmp/pitaya1"

    # Try and connect to the redpitaya
    rp_ip = "192.168.1.100" # = discover(rp_mac)
    response = os.system(
        "echo root | sshfs -o "
        "password_stdin root@192.168.1.239:/ /tmp/pitaya")

    # Successfully connected rp
    if response == 0:
        session.rp = {
            'connected': True,
            'ip': rp_ip
        }
        flash("Successfully connected %s with MAC: %s" % (rp_name, rp_mac)) 
    else:
        flash("Could not connect Red Pitaya. Please check your connection.")

    return render_template('index.html', error="error")


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
