# app/reader/views.py
# This file is for the Sleepscreen (/) and choose screen (/chooselogin)

from . import scanner
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
import os
from time import sleep
import json
from ..sqlite.operation_functions import Operations
from ..temp import Temp

temp = Temp()


@scanner.route('/scan/<method>', methods = ['GET', 'POST'])
def scan(method):
    # POST / FETCH to update this side if scanner scanned something
    if request.method == 'POST':
        if 'back' in request.form:
            temp.temp(False, "write_status", "w")
            sleep(1)
            return redirect(url_for(method + '.' + method + '_'))
    else:
        temp.temp(True, "write_status", "w")
        return render_template('scanner/scan_' + method + '.html')

@scanner.route('/getid', methods = ['GET'])
def getID():
    while True:
        if temp.temp(None, "write_status", "r") == False:
            return None
        try:
            data = temp.temp(None, "id", "r")
        except:
            print("File is empty or reading Error")
            print("sleeping for 0.5 seconds")
            sleep(0.5)
        else:
            if "0x0" in data:
                temp.temp(False, "write_status", "w")
                return json.dumps({"code":"0x0"})
            id = data
            session['id'] = id
            temp.temp(False, "write_status", "w")
            return json.dumps({"code":"0x1"})

@scanner.route('/checkData', methods = ['GET'])
def checkData():
    if 'id' in session:
        print(session['id'])
        print(type(session['id']))
        id = int(session['id'])
        print("sleeping for 0.5 seconds")
        sleep(0.5)
        try:
            op = Operations()
            print('Database connected')

            userId = op.check_user_exist_id(id)
            bookId = op.check_book_exist_id(id)
            if userId:
                print("ID is connected with a user")
                print(userId)
                code = {'code':'1x0', "userId":userId}
            elif bookId:
                print("ID is connected with a book")
                print(userId)
                code = {'code':'1x1', "bookId":bookId}
            else:
                print("ID is not connected, ready too use")
                code = {'code':'1x2'}
        finally:
            print("Checking done")
            op.conn.close()
            print("Database closed")
            jsoncode = json.dumps(code)
            return jsoncode
    else:
        print('No id in session')
        return json.dumps({'code': '1x3'})