# app/home/views.py

# This routing script is for the first screen (sleepscreen?!)


from . import home
from flask import Flask, render_template

@home.route('/', methods = ['GET'])
def index():
    return render_template('home/index.html')