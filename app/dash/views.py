# app/dash/views.py

from . import dash
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
from ..sqlite.operation_functions import Operations
from time import sleep

#rename x pls!
@dash.route('/dash', methods = ['POST', 'GET'])
def dash_():
    # Load data from Database!

    op = Operations()

    userData = op.get_data_by_userId(session['userId'])
    userFirst = userData[0][1]
    userLast = userData[0][2]
    userEmail = userData[0][3]

    bookData = op.get_book_data_by_userId(session['userId'])

    return render_template('dash/dash.html', userFirst = userFirst, userLast = userLast, userEmail=userEmail, bookData = bookData)

@dash.route('/logout', methods = ["POST"])
def logout():
    # Pop sessions
    session.pop("userId", None)
    sleep(2.4)
    return redirect(url_for('home.index'))

@dash.route('dash/get_data', methods = ['POST'])
def get_data():

    req = request.get_json()

    print(req)

    op = Operations()
    
    bookData = op.get_book_data_by_userId(session['userId'])

    res = make_response(render_template('dash/dash_update.html', ), 200)
    return res