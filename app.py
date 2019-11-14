from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
import sqlite3
from time import sleep
import sys
import random
import requests
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522


app = Flask(__name__)

app.secret_key = '56732356754345678'

# reader = SimpleMFRC522()

# def clean_GPIO():
#     print("\n\nProgramm has been terminated...")
#     GPIO.cleanup()
#     print("GPIO has been cleaned up...")

@app.route('/', methods = ['POST', 'GET'])
def index():

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
            return render_template('scan.html')
        elif 'back2' in request.form:
            return render_template('firstuse.html')
        else:
            return render_template('firstuse.html')
    else:
        return render_template('firstuse.html')        


@app.route('/first/form')
def cardrecognized():
    # Needs input
    
    id = session['id_f']
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
        session.pop('id_f', None)
        print('Session with the key id_f got cleaned up')
        return email
    else:
        return "doesn't work"

@app.route('/fu-done ')
def doneFirst():
    # Needs name of user
    pass
    
@app.route('/scan', methods = ['GET'])
def scan():
    if request.method == 'GET':
        try:
            # id = str(reader.read_id())
            id = "3464356456784"
        except:
            pass
        else:
            #Has to changed
            # clean_GPIO()
            session['id_f'] = id
            return redirect(url_for('checkData'))
    else:
        return ('something went wrong')

@app.route('/checkData')
def checkData():
    if 'id_f' in session:
        id = session['id_f']
        # Check id
        print('yep')
        return '1'
    elif 'id_l' in session:
        # for login
        pass
    elif 'id_b' in session:
        # for scanning books
        pass
    else:
        print('Something went wrong')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

