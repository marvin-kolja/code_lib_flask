# app/dash/views.py

from . import dash
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
from ..sqlite.operation_functions import Operations
from time import sleep
import json
# Import socket module 
import socket 

# Settings for socket communication
####################################
# local host IP '127.0.0.1' 
HOST = '127.0.0.1'
# Define the port on which you want to connect 
PORT = 12345
####################################


@dash.route('/dash', methods = ['POST', 'GET'])
def dash_():

    # For the first book update this session needs to be False -> see: def get_data()
    session['dash'] = False

    # Initilize Database
    op = Operations()

    # Load data from Database!
    userData = op.get_data_by_userId(session['userId'])
    userFirst = userData[0][1]
    userLast = userData[0][2]
    userEmail = userData[0][3]

    return render_template('dash/dash.html', userFirst = userFirst.capitalize(), userLast = userLast.capitalize(), userEmail=userEmail)

@dash.route('/logout', methods = ["POST"])
def logout():

    # Pop sessions
    session.pop("userId", None)
    session.pop('dash', None)

    # This sleep is there for keeping 
    # the "Goodbye" screen for the amount of time
    sleep(2.4)

    return redirect(url_for('home.index'))

@dash.route('/dash/get_data', methods = ['GET'])
def get_data():

    # Initilize Database
    op = Operations()


    if session['dash']:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

            # connect to server on local computer 
            s.connect((HOST,PORT)) 

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
        except:
            return json.dumps({"code":"0x00"})
        else:
            if id == session['id']:
                pass
            else:
                check = op.check_book_userId(id, session['userId'])
                if check == "0x0":
                    pass
                elif check == True:
                    op.update_book_userId_admin(id)
                else:
                    op.connect_userId_with_book(id, session['userId'])

    bookData = op.get_book_data_by_userId(session['userId'])

    res = ''
    i = 0
    if bookData == {}:
        res += """<div class="flex-item"><div class="center">No books, yet...</div></div>"""
    else:
        for book in bookData:
            i += 1
            res += f"""<div class="flex-item"><div class="left">{bookData[book][0]}. {bookData[book][1]}, {bookData[book][2]}</div><div class="right">Rent Date: {bookData[book][3]}, Return Date: {bookData[book][4]}</div></div><hr class="lis">"""
    print(res)

    session['dash'] = True

    return json.dumps({"code":res})