# app/reader/views.py
# This file is for the Sleepscreen (/) and choose screen (/chooselogin)

from . import scanner
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
import os
from time import sleep
import json




@scanner.route('/scan/<method>', methods = ['GET', 'POST'])
def scan(method):
    global stop_writing_id
    # POST / FETCH to update this side if scanner scanned something
    if request.method == 'POST':
        if 'back' in request.form:
            os.system('rm temp/data.txt')
            stop_writing_id = True
            sleep(1)
            return redirect(url_for('signup.signup_'))
    else:
        os.system('rm temp/data.txt')
        stop_writing_id = False
        return render_template('scan.html')

@scanner.route('/getid', methods = ['GET'])
def getID():
    while True:
        global stop_writing_id
        if stop_writing_id == True:
            return None
        try:
            with open('temp/data.txt') as json_file:
                data = json.load(json_file)
        except:
            print("File is empty or reading Error")
            print("sleeping for 0.5 seconds")
            sleep(0.5)
        else:
            if 'code' in data:
                if data['code'] == '0x0':
                    os.system('rm temp/data.txt')
                    stop_writing_id == True
                    return json.dumps({"code":"0x0"})
                print("Another error occured")
                print(data['code'])
                return None
            id = data['id']
            os.system('rm temp/data.txt')
            session['id'] = id
            stop_writing_id == True
            return json.dumps({"code":"0x1"})