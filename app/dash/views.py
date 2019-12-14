# app/dash/views.py

from . import dash
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
from ..sqlite.operation_functions import Operations
from time import sleep
import json
from ..temp import Temp

temp = Temp()

#rename x pls!
@dash.route('/dash', methods = ['POST', 'GET'])
def dash_():
    session['dash'] = False
    # Enable Scanner
    temp.temp(True, "write_status", "w")
    # Load data from Database!

    op = Operations()

    userData = op.get_data_by_userId(session['userId'])
    userFirst = userData[0][1]
    userLast = userData[0][2]
    userEmail = userData[0][3]

    return render_template('dash/dash.html', userFirst = userFirst, userLast = userLast, userEmail=userEmail)

@dash.route('/logout', methods = ["POST"])
def logout():
    # Pop sessions
    session.pop("userId", None)
    session['dash'] = False
    # Disable Scanner
    temp.temp(False, "write_status", "w")

    sleep(2.4)
    return redirect(url_for('home.index'))

@dash.route('/dash/get_data', methods = ['GET'])
def get_data():
    # req = request.get_json()

    # print(req)

    op = Operations()

    if session['dash']:
        while True:
            if temp.temp(None, "write_status", "r") == False:
                return '0x0'
            try:
                data = temp.temp(None, "id", "r")
            except:
                print("File is empty or reading Error")
                print("sleeping for 0.5 seconds")
                sleep(0.5)
            else:
                if "0x0" in data:
                    return json.dumps({"code":"0x0"})
                else:
                    id = data
                    op.connect_userId_with_book(id, session['userId'])
                    break

    bookData = op.get_book_data_by_userId(session['userId'])

    res = ''
    i = 0

    for book in bookData:
        i += 1
        res += f"""<div class="flex-item"><div class="left">{bookData[book][0]}. {bookData[book][1]}, {bookData[book][2]}</div><div class="right">Rent Date: {bookData[book][3]}, Return Date: {bookData[book][4]}</div></div><hr class="lis">"""
    print(res)

    session['dash'] = True

    return json.dumps({"code":res})