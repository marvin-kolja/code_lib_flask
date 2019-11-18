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
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time


app = Flask(__name__)



timeout = 30

global stop_threads
stop_threads = True

def clean_GPIO():
    print("\n\nProgramm has been terminated...")
    GPIO.cleanup()
    print("GPIO has been cleaned up...")



# @app.before_first_request
# def active_job():
#     print("Hello")
def run_job():
    while True:
        if stop_threads == True:
            break
        try:
            print('ready to scan')
            reader = SimpleMFRC522()
            print('scanner initialized')
            id = reader.read_id()
            print('Scan successfull')
            # id = "215531341298"
            if stop_threads == True:
                break
            id = str(id)
        except:
            return json.dumps({"code":"0x0"})
        else:
            #Has to changed
            print("convert successfull")
            clean_GPIO()  
            data = {'id':id}
            r = requests.post('http://localhost/scan', json=data)
            with open('temp/data.txt', 'w') as file:
                json.dump(data, file)
            print("id printed to file")
    
thread = threading.Thread(target=run_job)


@app.route('/', methods = ['POST', 'GET'])
def index():
    x = datetime.now()
    x = x.strftime("%a" + " " + "%H" + ":" + "%M")

    if request.method == 'POST':
        if request.form['start'] == '':
            return redirect(url_for('chooselogin'))
        else:
            return render_template('index.html', date = x)
    else:
        return render_template('index.html', date = x)

# @app.route('/scanner')
# def scanner():
#     session['scanning'] = True
#     while True:
#         try:
#             print('ready to scan')
#             reader = SimpleMFRC522()
#             print('scanner initialized')
#             id = reader.read_id()
#             print('Scan successfull')
#             # id = "215531341298"
#             session.pop('scanning')
#             id = str(id)
#         except:
#             print("Scan Error")
#             return json.dumps({"code":"0x0"})
#         else:
#             #Has to changed
#             print("convert successfull")
#             clean_GPIO()
#             print('Session successfull')    
#             data = {'id':id}
#             with open('temp/data.txt', 'w') as file:
#                 json.dump(data, file)
#             return 'worked'

@app.route('/chooselogin', methods = ['POST', 'GET'])
def chooselogin():
    if request.method == 'POST':
        if request.form['button'] == 'Log in':
            return redirect(url_for('login'))
        elif request.form['button'] == 'First use':
            return redirect(url_for('firstuse'))
        else:
            return render_template('choose.html')

    else:
        return render_template('choose.html')

@app.route('/first', methods = ['POST', 'GET'])
def firstuse():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('chooselogin'))
        elif 'next' in request.form:
            """Load different .html (e.g. scancard) This one should include a different POST button for scanning"""
            return redirect(url_for('scan'))
        else:
            return render_template('firstuse.html')
    else:
        return render_template('firstuse.html')        


@app.route('/first/form')
def cardrecognized():
    # Needs input
    
    id = session['id']
    return render_template('email.html', id=id)


@app.route('/first/confirm', methods = ['POST', 'GET'])
def emailconfirm():
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

@app.route('/fu-done ')
def doneFirst():
    # Needs name of user
    pass
    
@app.route('/scan', methods = ['GET', 'POST'])
def scan():
    # POST / FETCH to update this side if scanner scanned something
    if request.method == 'POST':
        if 'back2' in request.form:
            os.system('rm temp/data.txt')
            stop_threads = True
            thread.join()
            return redirect(url_for('firstuse'))
        if 'id' in request.args:
            data = request.get_json()
            id = data['id']
            session['id'] = id
            return render_template('scan.html', id = id)
        else:
            os.system('rm temp/data.txt')
            thread.start()
            return render_template('scan.html', id = '000')
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

@app.route('/checkData', methods = ['GET'])
def checkData():
    if 'id' in session:
        id = int(session['id'])
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
        
    elif 'id_l' in session:
        # for login
        pass
    elif 'id_b' in session:
        # for scanning books
        pass
    else:
        print('Something went wrong')



if __name__ == "__main__":
    app.secret_key = '56732356754345678'
    app.run(debug=True, host='0.0.0.0', threaded=True)

