from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import sqlite3
from time import sleep
import sys
import random
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


app = Flask(__name__)
reader = SimpleMFRC522()

@app.route('/')
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

@app.route('/first/intro', methods = ['POST', 'GET'])
def firstuse():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('chooselogin'))
        elif 'next' in request.form:
            return redirect(url_for('scancardFirst'))
        else:
            return render_template('firstuse.html')
    else:
        return render_template('firstuse.html')


@app.route('/first/scancard')
def scancardFirst():
    try:
        id = str(reader.read_id())
    except:
        # print ("Something went wrong with with the reader...")
        raise
    else:
        return id

@app.route('/first/form')
def cardrecognized():
    # Needs input
    return render_template('email.html')


@app.route('/first/confirm', methods = ['POST', 'GET'])
def emailconfirm():
    # Has to talk to the e-mail confirmation...
    # For the MVP just talk to database
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email = (first_name + last_name + "@code.berlin")
        return email
    else:
        return "doesn't work"

@app.route('/fu-done ')
def doneFirst():
    # Needs name of user
    pass



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

