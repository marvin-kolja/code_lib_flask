# app/id_handler/views.py

# This script is to handle with the UID
#   1. get the UID from the scanner (via socket communication)
#   2. check if the UID is valid

from . import id_handler
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
import os
from time import sleep
import json
from ..sqlite.operation_functions import Operations
# Import socket module 
import socket 

# Settings for socket communication
####################################
# local host IP '127.0.0.1' 
HOST = '127.0.0.1'
# Define the port on which you want to connect 
PORT = 12345
####################################

@id_handler.route('/getid', methods = ['GET'])
def getID():

    # connecting with scanner-socket that runs as a service on the Rpi
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

        # connect to server on local computer 
        s.connect(('127.0.0.1',12345)) 

        # message you send to server
        ''' PLEASE CHANGE '''
        message = "shaurya says geeksforgeeks"


        # message sent to server (could be for auth purpose)
        s.send(message.encode('ascii')) 

        # messaga received from server 
        data = s.recv(1024) 

        # print the received message 
        print('Received from the server :',str(data.decode('ascii'))) 

        # put the UID into a session
        session['id'] = str(data.decode('ascii'))

        s.close()

        # return success code to frontend (0x00 = failure ; 0x01 = success)
        return json.dumps({"code":"0x01"})
    except:
        return json.dumps({"code":"0x00"})

@id_handler.route('/checkData', methods = ['GET'])
def checkData():

    # Continue only if ID exists in session (else there is something wrong)
    if 'id' in session:

        # Log stuff to terminal for testing purpose
        print(session['id'])
        print(type(session['id']))

        # Transform the UID to an integer
        ''' error handler may be needed '''
        id = int(session['id'])

        try:
            op = Operations()
            print('Database connected')

            userId = op.check_user_exist_id(id)
            bookId = op.check_book_exist_id(id)
            if userId:
                print("ID is connected with a user")
                print(userId)
                code = {'code':'0x01', "userId":userId}
            elif bookId:
                print("ID is connected with a book")
                print(userId)
                code = {'code':'0x02', "bookId":bookId}
            else:
                print("ID is not connected, ready too use")
                code = {'code':'0x03'}
        finally:
            print("Checking done")
            op.conn.close()
            print("Database closed")
            jsoncode = json.dumps(code)
            return jsoncode
    else:
        print('No id in session')
        return json.dumps({'code': '0x00'})