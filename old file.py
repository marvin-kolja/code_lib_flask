from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g

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
from sqlite.users import User

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
    if request.args.get("err"):
        err = request.args.get("err")
        email = request.args.get("email")
        return render_template('email.html', err=err, email=email)
    else:
        return render_template('email.html')

@app.route('/signup/email-send', methods = ['POST', 'GET'])
def signupEmailSend():
    # send email
    # For the MVP just return redirect to confirm
    if request.method == 'POST':
        first_name = request.form['first'].lower()
        last_name = request.form['last'].lower()
        email = (first_name + '.' + last_name + "@code.berlin")

        user = User(first_name, last_name, None)

        op = Operations()
        if op.check_user_exist_name(user):
            session['userFirst'] = first_name
            session['userLast'] = last_name
            session['userId'] = op.check_user_exist_name(user)
            return redirect(url_for("signupConfirm"))
        else:
            return redirect(url_for("signupForm", err="err1", email=email))
    else:
        return "Something went wrong"
    # return redirect(url_for('signupConfirm'))
    return "Something went wrong"


@app.route('/signup/confirm', methods = ['POST', 'GET'])
def signupConfirm():
    # screen: Waiting for confirmation...
    return render_template('confirm.html', userId = session['userId'], first = session['userFirst'], last = session['userLast'])

@app.route('/signup/checkconfirm', methods = ['GET'])
def checkConfirm():
    # check Database for confirmation
    op = Operations()
    while True:
        # check if user is confirmed (database)
        if op.check_confirm_with_userId(session['userId']) == 1:
            # input user
            user = User(session['userFirst'], session['userLast'], None)
            # id
            id = session['id']
            # check user
            connectId = op.connect_ID_with_user(user, id)
            if connectId:
                # Delete session
                session.pop('id', None)
                print('Session with the key id got cleaned up')
                return redirect(url_for("signupDone"))
        else:
            print('not confirmed yet')
        sleep(3)

@app.route('/confirmlink')
def confirm():
    # has to be changed with email etc
    # session has to different aswell (userId inside the link)
    op = Operations()
    op.confirm_with_userId(session['userId'])
    return 'Confirmed'

@app.route('/signup/done')
def signupDone():
    userFirst = (session['userFirst']).capitalize() 
    op = Operations()
    if op.reset_confirm_with_userId(session['userId']):
        print("userConfirm has been reset")
    session.pop('userId', None)
    session.pop('userFirst', None)
    session.pop('userLast', None)
    print("session has been deleted")
    return render_template('done.html', userFirst=userFirst)
    
@app.route('/scan/<method>', methods = ['GET', 'POST'])
def scan(method):
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
    app.run(debug=True, host='libscanner.0.0.0.0', threaded=True)
