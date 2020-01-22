# app/signup/views.py

from . import signup
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response, g
import requests
from datetime import datetime
from ..sqlite.operation_functions import Operations
from ..sqlite.users import User
from time import sleep
      


@signup.route('/signup/form')
def signupForm():
    # Needs input
    if request.args.get("err"):
        err = request.args.get("err")
        email = request.args.get("email")
        return render_template('signup/email.html', err=err, email=email)
    else:
        return render_template('signup/email.html')

@signup.route('/signup/email-send', methods = ['POST', 'GET'])
def signupEmailSend():
    # send email
    # For the EXPO MVP Just add a user to the Database
    if request.method == 'POST':
        first_name = request.form['first'].lower()
        last_name = request.form['last'].lower()
        email = (first_name + '.' + last_name + "@code.berlin")

        user = User(first_name, last_name, session['id'])

        session['userFirst'] = first_name
        op = Operations()
        if op.check_user_exist_name(user):
            op.update_id(op.check_user_exist_name(user), session['id'])
            session['userId'] = op.check_user_exist_name(user)
            return redirect(url_for('signup.signupDone'))
        else:
            op.insert_user(user, email)
            session['userId'] = op.check_user_exist_name(user)
            return redirect(url_for('signup.signupDone'))
        

        # op = Operations()
        # if op.check_user_exist_name(user):
        #     session['userFirst'] = first_name
        #     session['userLast'] = last_name
        #     session['userId'] = op.check_user_exist_name(user)
        #     return redirect(url_for("signup.signupConfirm"))
        # else:
        #     return redirect(url_for("signup.signupForm", err="err1", email=email))
    else:
        return "Something went wrong"
    # return redirect(url_for('signupConfirm'))
    return "Something went wrong"


@signup.route('/signup/confirm', methods = ['POST', 'GET'])
def signupConfirm():
    # screen: Waiting for confirmation...
    return render_template('signup/confirm.html', userId = session['userId'], first = session['userFirst'], last = session['userLast'])

@signup.route('/signup/checkconfirm', methods = ['GET'])
def checkConfirm():
    # check Database for confirmation
    op = Operations()
    while True:
        # check if user is confirmed (database)
        if op.check_confirm_with_userId(session['userId']) == 1:
            # input user
            user = User(session['userFirst'], session['userLast'], None)
            # id
            id = session['id']
            # check user
            connectId = op.connect_ID_with_user(user, id)
            if connectId:
                # Delete session
                session.pop('id', None)
                print('Session with the key id got cleaned up')
                return redirect(url_for("signup.signupDone"))
        else:
            print('not confirmed yet')
        sleep(3)

@signup.route('/confirmlink')
def confirm():
    # has to be changed with email etc
    # session has to different aswell (userId inside the link)
    op = Operations()
    op.confirm_with_userId(session['userId'])
    return 'Confirmed'

@signup.route('/signup/done')
def signupDone():
    userFirst = (session['userFirst']).capitalize() 
    op = Operations()
    if op.reset_confirm_with_userId(session['userId']):
        print("userConfirm has been reset")
    session.pop('userId', None)
    session.pop('userFirst', None)
    session.pop('userLast', None)
    print("session has been deleted")
    return render_template('signup/done.html', userFirst=userFirst)