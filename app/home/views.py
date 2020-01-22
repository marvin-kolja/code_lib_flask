# app/home/views.py
# This file is for the Sleepscreen (/) and choose screen (/chooselogin)


from . import home
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
from datetime import datetime
from ..temp import Temp
import os

temp = Temp()

@home.route('/', methods = ['GET'])
def index():
    return render_template('home/home.html')