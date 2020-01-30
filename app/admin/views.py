# app/dash/views.py

from . import admin
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
from ..sqlite.operation_functions import Operations
from time import sleep

@admin.route('/admin', methods = ['GET'] )
def admin_():
    """ admin gets here from home screen """
    if session['admin']:
        return render_template('admin/admin.html')
    else:
        return 'Admin session not active!'
