# app/dash/views.py

from . import dash
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
from ..sqlite.operation_functions import Operations

@dash.route('/dash', methods = ['POST', 'GET'])
def dash_():
    # Load data from Database!

    op = Operations()

    userData = op.get_data_by_userId(g.userId)
    g.userFirst = userData[0][1]
    g.userLast = userData[0][2]
    g.userEmail = userData[0][3]

    bookData = op.get_book_data_by_userId(g.userId)



    return render_template('dash/dash.html', userFirst = g.userFirst, userLast = g.userLast, userEmail=g.userEmail,bookData = bookData)