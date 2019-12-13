# app/home/views.py
# This file is for the Sleepscreen (/) and choose screen (/chooselogin)


from . import home
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
from datetime import datetime
from ..temp import Temp
import os

temp = Temp()

@home.route('/', methods = ['POST', 'GET'])
def index():

    temp.temp(False, "write_status", "w")
    x = datetime.now()
    x = x.strftime("%a" + " " + "%H" + ":" + "%M")

    if request.method == 'POST':
        if request.form['start'] == '':
            return redirect(url_for('home.chooselogin'))
        else:
            return render_template('home/home.html', date = x)
    else:
        return render_template('home/home.html', date = x)

@home.route('/chooselogin', methods = ['POST', 'GET'])
def chooselogin():
    if request.method == 'POST':
        if request.form['button'] == 'Log in':
            return redirect(url_for('scanner.scan', method='login'))
        elif request.form['button'] == 'Sign up':
            return redirect(url_for('signup.signup_'))
        else:
            return render_template('home/choose.html')
    else:
        return render_template('home/choose.html')