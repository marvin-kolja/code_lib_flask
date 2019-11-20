from flask import Flask, render_template, redirect, url_for, request, session

import threading

from datetime import datetime

import sqlite3

from time import sleep

import os

import sys

import random

import requests

import json

from sqlite.operation_functions import Operations

import time

from reader import Reader


app = Flask(__name__)

timeout = 30


def w_temp(data):
    with open('temp/data.txt', 'w') as file:
        json.dump(data, file)
    print("id printed to file")


def run_job():
    global stop_writing_id
    while True:
        reader = Reader()
        returned = reader.read()
        if returned == '0x0':
            data = {"code": returned}
            print("Scanner error!")
            w_temp(data)
            continue
        else: 
            data = returned
            if stop_writing_id == False:
                w_temp(data)
    
thread = threading.Thread(target=run_job)

@app.before_first_request
def active_job():
    global stop_writing_id
    stop_writing_id = True
    print("Variables are global")
    thread.start()
    print("Thread started")

@app.route('/', methods = ['POST', 'GET'])
def index():
    global stop_writing_id
    stop_writing_id = True
    
    x = datetime.now()
    x = x.strftime("%a" + " " + "%H" + ":" + "%M")

    if request.method == 'POST':
        if request.form['start'] == '':
            return redirect(url_for('chooselogin'))
        else:
            return render_template('index.html', date = x)
    else:
        return render_template('index.html', date = x)


@app.route('/chooselogin', methods = ['POST', 'GET'])
def chooselogin():
    if request.method == 'POST':
        if request.form['button'] == 'Log in':
            return redirect(url_for('login'))
        elif request.form['button'] == 'Sign up':
            return redirect(url_for('signup'))
        else:
            return render_template('choose.html')
    else:
        return render_template('choose.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('chooselogin'))
        elif 'next' in request.form:
            """Load different .html (e.g. scancard) This one should include a different POST button for scanning"""
            return redirect(url_for('scan'))
        else:
            return render_template('signup.html')
    else:
        return render_template('signup.html')        


@app.route('/signup/form')
def signupForm():
    global stop_writing_id
    stop_writing_id = True
    # Needs input
    id = session['id']
    return render_template('email.html', id=id)


@app.route('/signup/confirm', methods = ['POST', 'GET'])
def signupConfirm():
    # Has to talk to the e-mail confirmation...
    # For the MVP just talk to database
    if request.method == 'POST':
        first_name = request.form['first'].lower()
        last_name = request.form['last'].lower()
        email = (first_name + '.' + last_name + "@code.berlin")
        # Put inside database

        # Delete session
        session.pop('id', None)
        print('Session with the key id got cleaned up')
        return email
    else:
        return "doesn't work"

@app.route('/signup/done ')
def signupDone():
    # Needs name of user
    pass
    
@app.route('/scan', methods = ['GET', 'POST'])
def scan():
    global stop_writing_id
    # POST / FETCH to update this side if scanner scanned something
    if request.method == 'POST':
        if 'back' in request.form:
            os.system('rm temp/data.txt')
            stop_writing_id = True
            sleep(1)
            return redirect(url_for('signup'))
        else:
            os.system('rm temp/data.txt')
            stop_writing_id = False
            return render_template('scan.html')
    # elif request.method == 'GET':
    #     # SHOULD NOT BE ACCESABLE FOR USERS
    #     session['scanning'] = True
    #     os.system('rm temp/data.txt')
    #     scanning = session.get('scanning')
    #     print(scanning)
    #     if scanning == True:
    #         print("Scanner already scans")
    #     else:
    #         try:
    #             r = requests.get('http://localhost:5000/scanner', timeout=5)
    #             print(r.text)
    #         except requests.exceptions.RequestException:
    #             pass
    #     timeout_start = time.time()
    #     while True:
    #         if time.time() > timeout_start + timeout:
    #             return json.dumps({'code':'0x2'})
    #         else:
    #             try:
    #                 with open('temp/data.txt') as json_file:
    #                     data = json.load(json_file)
    #             except:
    #                 print("File is empty or reading Error")
    #             else:
    #                 id = data['id']
    #                 os.system('rm temp/data.txt')
    #                 session['id'] = id
    #                 return json.dumps({"code":"0x1"})
    #         print("no id")
    #         sleep(1)
    #         continue
    # else:
    #     return 'something went wrong'

@app.route('/getid', methods = ['GET'])
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

@app.route('/checkData', methods = ['GET'])
def checkData():
    if 'id' in session:
        print(session['id'])
        print(type(session['id']))
        id = int(session['id'])
        print("sleeping for 0.5 seconds")
        sleep(0.5)
        try:
            op = Operations()
            print('Database connected')

            userId = op.check_user_exist_id(id)
            bookId = op.check_book_exist_id(id)
            if userId:
                print("ID is already connected with a user")
                print(userId)
                code = {'code':'1x0', "userId":userId}
            elif bookId:
                print("ID is already connected with a book")
                print(userId)
                code = {'code':'1x1', "bookId":bookId}
            else:
                print("ID is not connected, ready too use")
                code = {'code':'1x2'}
        finally:
            print("Checking done")
            op.conn.close()
            print("Database closed")
            jsoncode = json.dumps(code)
            return jsoncode

        # database_contents = ''
        # conn = sqlite3.connect('sqlite/library.db')
        # try:
        #     c = conn.cursor()
        #     rows = c.execute('SELECT * FROM book_book')
        #     for row in rows:
        #         database_contents += f"{row}\n\n"
        #     msg = 'Database Content test:' + database_contents
        # finally:
        #     return render_template('index.html', msg = msg)
        #     conn.close()
    else:
        print('No id in session')
        return json.dumps({'code': '1x3'})



if __name__ == "__main__":
    app.secret_key = '56732356754345678'
    app.run(debug=True, host='0.0.0.0', threaded=True)

