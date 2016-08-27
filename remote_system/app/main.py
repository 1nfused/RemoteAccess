 
import os
import datetime
import json
import logging
import requests
import urllib2
import subprocess

from flask import Flask, render_template, \
    request, url_for, redirect, session, flash, g, jsonify

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship

from requests.exceptions import HTTPError, ConnectionError
from time import gmtime, strftime
from threading import Thread
import multiprocessing
from time import sleep
from math import *

import constants

app = Flask(__name__, template_folder='static/templates')
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

    def __init__(self, username, password, name, email, role=False):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.role = role


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
    db.session.commit() 
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
                    'ip': None,
                    'action': 'connect'
                }
                session['rp'] = rp
                session['logged_in'] = True
                session['logged_user'] = user.username
                session['first_log'] = False;
                return render_template('index.html', error=error)
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
    avaliable_apps = {}

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
                if rp:
                    avaliable_rp[split[0]] = rp.name
                    break 
            else:
                continue
        except IndexError:
            continue

    session['avaliable_pitaya'] = avaliable_rp
    response = {
        'success': True,
        'data': {
            'avaliable_rp': avaliable_rp, 
            'avaliable_apps': avaliable_apps }
    }

    return jsonify(response), 200

'''
@app.route('/logs', methods=['GET', 'POST'])
def logs():
    return render_template('logs.html')
'''


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    post_request = json.loads(request.data.decode())

    response = {
        'success': False,
        'msg': ''
    }

    add_type = post_request.get('type')
    
    print post_request

    if add_type == 'user':
        username = post_request.get('data')['username']
        if User.query.filter(User.username == username).first():
            print "USERNAME exists"
            response['msg'] = \
                "User with username %s already exists" % username
            return jsonify(response), 504

        name = post_request.get('data')['name']
        surname = post_request.get('data')['surname']
        email = post_request.get('data')['email']

        if not name or not surname or not email:
            print "ALL FIELDS"
            response['msg'] = "All fields are required!"
            return jsonify(response), 504

        # Create user
        user = User(username, "root", name, email)
        db.session.add(user)
        db.session.commit()
        
        # Flash response
        response = { 
            'success': True,
            'msg': 'Successfully created user %s' % (username) }

        return jsonify(response), 200
    
    elif add_type == 'pitaya':
        rp_name = \
            post_request.get('data')['name']
        rp_mac = \
            post_request.get('data')['mac']

        # Check if MAC is correct right away
        if len(rp_mac) != 17:
            response['msg'] = "Invalid MAC address!"
            return jsonify(response), 504

        if not rp_name or not rp_mac:
            response['msg'] = "All fields are require!"
            return jsonify(response), 504

        if RedPitaya.query.filter(RedPitaya.mac == rp_mac).first():
            response['msg'] = "RedPitaya already exists!"
            return jsonify(response), 504
            
        rp = RedPitaya(rp_name, rp_mac)
        db.session.add(rp)
        db.session.commit()

        response = {
            'success': True,
            'msg': "Successfully created Red Pitaya %s" % rp_name }
    return jsonify(response), 200

@app.route('/gpio', methods=['GET'])
def gpio():
    # Read GPIO file from mounted RP
    pass

# Opens up the registers file and reads registers
@app.route('/registers', methods=['POST', 'GET'])
def registers():
    registers = None
    
    try:
        rp_name = session.get('rp')['name']
        registers = get_register_data(rp_name)
    except KeyError:
        response = {
            'data': None,
            'success': False
        }

    response = {
        'data': registers,
        'success': True
    }
    return jsonify(response), 200


# One of the main functions
@app.route('/connect', methods=['POST'])
def connect():

    rp = json.loads(request.data.decode())
    rp_ip = rp['ip']
    rp_name = rp['name'].replace(' ', '')
    rp_mount_point = '%s/%s' % (constants.RP_SSHFS_BASE_MOUNT_DIR, rp_name)

    # Form {'name': ['icon', 'link', 'description']}
    avaliable_apps = {}

    if not os.path.exists(rp_mount_point):
        os.makedirs(rp_mount_point)

    response = os.system(
        "echo root | sshfs -o password_stdin root@%s:/ /tmp/%s" \
        % (rp_ip, rp_name))

    # Successfully connected rp
    if response == 0:
        msg = "Successfully connected %s pitaya" % (rp_name)
        mount_path = "/tmp/%s/" % rp_name
        file = open(
            (mount_path + constants.RP_VERSION_PATH + 'version.txt'),
            "r")

        session['rp'] = {
            'connected': True,
            'ip': rp_ip,
            'name': rp_name,
            'active': strftime("%d-%m-%Y %H:%M", gmtime()),
            'version': '0.94',
            'fs': 'Ubuntu',
            'fpga': '0.94',
            'action': 'disconnect'
        }

        # Get avaliable free applications list
        apps_directory = mount_path + constants.RP_APPS_DIRECTORY
        rp_list = \
            subprocess.Popen(
                ['ls', apps_directory,],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)

        stdout, stderr = rp_list.communicate()
        for app in stdout.split('\n'):
            if app in constants.RP_GLOBALY_AVALIABLE_APPS:
                icon_link = ('file://///%s%s/info/icon.png' % (apps_directory, app))
                start_link = ('http://%s/%s/?type=run' % (rp_ip, app))
                description = "" # Maybe implement
                avaliable_apps[app] = {
                    'icon': icon_link, 
                    'start_app': start_link, 
                    'desc': description}

        # Start registers function          
        # pool_register_data(rp_ip)

        # Create response object
        response = {
            'success': True,
            'data': {
                'msg': msg,
                'rp': session['rp'],
                'apps': avaliable_apps }
        }
        return jsonify(response), 200
    else:
        error = "Could not connect Red Pitaya. Please check your connection."
        return jsonify(
            response={
                'success': False, 
                'data' : { 'error': error }}), 504


@app.route('/disconnect', methods=['POST'])
def disconnect_rp():
    print "DISCONECTING PITAYA"
    rp = json.loads(request.data.decode())
    rp_name = rp['name'].replace(' ', '')

    response = os.system(
        'echo root | fusermount -o password_stdin -u /tmp/%s' % \
        rp_name)

    if response != 0:
        flash("Unable to disconnect pitaya %s" % rp_name)
        pass

    session['rp'] = {
        'connected': False,
        'ip': '',
        'name': '',
        'active': '',
        'version': '',
        'fs': '',
        'fpga': '',
        'action': 'connect'
    }

    flash("Successfully disconnected Red Pitaya %s" % rp_name)
    return render_template(
        'index.html', response={'action': 'connect'})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    return redirect(url_for('/'))



@app.route('/latency')
def latency():
    queue = multiprocessing.Queue()
    thread_ = \
        Thread(
            target=latency_thread,
            name="latency_tread",
            args=[queue])

    thread_.start()
    thread_.join()
    response = {
        'success': True,
        'data': str(queue.get())[:3] + 'ms'
    }
    return jsonify(response), 200


def latency_thread(queue):
    latency = '--'
    try:
        rp_ping = \
            subprocess.Popen(
                ['ping', '-q', '-c', '1', '192.168.1.239'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)

        stdout, stderr = rp_ping.communicate()
        latency = \
            stdout.split('\n')[4].split(' ')[3].split('/')[1]
    except Exception:
        print "EXCEPTION"

    # Put latency object in que    
    queue.put(latency)

def pool_register_data(rp_ip):
    print rp_ip
    response = os.system(
        'ssh -p root root@%s ' \
        '/opt/redpitaya/rp_registers' % rp_ip)
    if response != 0:
        print "Failed to execute registers script."
        return None
    return True

def get_register_data(pitaya_name):
    registers = {}
    file = open('/tmp/%s/opt/redpitaya/%s' % (
        pitaya_name, constants.REGISTER_DATA_FILE_NAME))

    mem_block_name = ""
    for line in file:
        if line == '\n':
            continue
        if line.replace('\n', '').isalpha():
            mem_block_name = line.replace('\n', '')
            registers[mem_block_name] = {}
        else:
            register_data = line.split(" ")
            binary_reg_val = list("{0:b}".format(int(register_data[1])))
            short_len = abs(len(binary_reg_val) - 32)
            register_value_32_bit = \
                [(lambda x: x)('0') for x in range(short_len)] + \
                    binary_reg_val + [register_data[1]]
            registers[mem_block_name][register_data[0]] = register_value_32_bit
    return registers

@app.before_request
def before_request():
        try:
            if session.get('logged_in'):
                g.user = session.get('logged_user')
        except AttributeError:
            return None

if __name__ == '__main__':
    # Global jinja functions
    # app.jinja_env.globals.update(connect=connect)
    app.run()
