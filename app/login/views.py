# app/signup/views.py

""" 
    Here should be a real login. (e.g. flask_login) 
    Hence it's just used by one user per time, it is not necessary!
"""

from . import login
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g

@login.route('/login/<userId>', methods = ['POST', 'GET'])
def login_(userId):
    session.pop('id', None)
    print('Session with the key id got cleaned up')
    session['userId'] = userId
    return redirect(url_for('dash.dash_'))

    