# app/signup/views.py

""" 
    Here should be a real login. (e.g. flask_login) 
    However, it's just used by one user per time. It may is not necessary!
"""

from . import login
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g

@login.route('/login/<userId>', methods = ['GET'])
def login_(userId):

    # put the userId in a session -> used at the dash
    session['userId'] = userId
    
    return redirect(url_for('dash.dash_'))

    