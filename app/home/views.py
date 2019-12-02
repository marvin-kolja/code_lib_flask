# app/home/views.py
# This file is for the Sleepscreen (/) and choose screen (/chooselogin)

from . import home
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
from datetime import datetime

@home.route('/', methods = ['POST', 'GET'])
def index():
    global stop_writing_id
    stop_writing_id = True
    
    x = datetime.now()
    x = x.strftime("%a" + " " + "%H" + ":" + "%M")

    if request.method == 'POST':
        if request.form['start'] == '':
            return redirect(url_for('home.chooselogin'))
        else:
            return render_template('home.html', date = x)
    else:
        return render_template('home.html', date = x)

@home.route('/chooselogin', methods = ['POST', 'GET'])
def chooselogin():
    if request.method == 'POST':
        if request.form['button'] == 'Log in':
            return redirect(url_for('login.login_'))
        elif request.form['button'] == 'Sign up':
            return redirect(url_for('signup.signup_'))
        else:
            return render_template('choose.html')
    else:
        return render_template('choose.html')