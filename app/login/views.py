# app/signup/views.py

""" 
    Here should be a real login. (e.g. flask_login) 
    Hence it's just used by one user per time, it is not necessary!
"""

from . import login
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g

@login.route('/login/<userId>', methods = ['POST', 'GET'])
def login_(userId):
    g.userId = userId
    return redirect(url_for('dash.dash_'))

    