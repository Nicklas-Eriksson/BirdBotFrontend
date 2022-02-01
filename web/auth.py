from asyncio import sleep
from cgitb import reset
from distutils.command.config import config
import imp
import random
import smtplib
from optparse import Values
from re import U
from threading import Thread
from token import VBAREQUAL
from unicodedata import name
from flask import Blueprint, render_template, request, flash, redirect, url_for
from web import Db, SecretKey
from web import utility
from web.utility import Edit as edit, Generate as generate
from web.models import User
from werkzeug.security import generate_password_hash as genHash, check_password_hash as checkHash
from flask_login import login_required, login_user, logout_user, current_user
import time
from web.serverClient import client as client
from web.dataProcess.analyzeData import Analyze
from itsdangerous import Serializer, TimedJSONWebSignatureSerializer as serializer
import os
from dotenv import load_dotenv

load_dotenv()
EmailAdress = os.getenv("EmailAdress")
EmailPassword = os.getenv("EmailPassword")
SecretKey = os.getenv("SecretKey")
auth = Blueprint('auth', __name__)
username = "Unknown"
token = None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.register'))
        elif request.form.get('forgotPass') == 'forgotPass':
            return redirect(url_for('auth.forgotPassword'))
        else:
            global username
            username = request.form.get('username')
            password = request.form.get('password')   

            if len(username) < 1:
                flash('You need to enter a username', category='error')
            elif len(password) < 1:
                flash('You need to enter a password', category='error')

            if username and password:
                credentials = edit.RemoveWhitespaceLogin(username, password)
                username = credentials[0]
                password = credentials[1]

                user = User.query.filter_by(username = username).first()
            
                if user:
                    if checkHash(user.password, password):
                        login_user(user, remember=True)
                        flash('Welcome!', category='success')
                        time.sleep(1.5)

                        return redirect(url_for('auth.search'))
                    else:
                        flash('Incorrect credentials', category='error')
                else:
                    flash('Incorrect credentials', category='error')
        
    return render_template('login.html')

tweets = "Empty"

@auth.route('/search')
@auth.route('/', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.logout'))        
        else:
            global searchWord
            global numberOfTweets
            global dataTuple
            global username

            searchWord = request.form.get('searchWord')
            numberOfTweets = request.form.get('numberOfTweets')
            searchFrom = request.form.get('searchFrom')

            if searchWord:
                searchWord = edit.RemoveWhitespaceSearch(searchWord)
                dataTuple = client.StartClient(searchWord, searchFrom, numberOfTweets)   
                             
                return redirect(url_for('auth.result'))

    else:
        return render_template('search.html', values=username)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.login'))

        else:
            email = request.form.get('email')
            firstName = request.form.get('firstName')
            surname = request.form.get('surname')
            username = request.form.get('username')
            password = request.form.get('password')
            repeatPassword = request.form.get('repeatPassword')

            if email and firstName and surname and username and password and repeatPassword:
                credentials = edit.RemoveWhitespaceRegister(email, firstName, surname, username, password, repeatPassword)
                email = credentials[0]
                firstName = credentials[1]
                surname = credentials[2]
                username = credentials[3]
                password = credentials[4]
                repeatPassword = credentials[5]
                userUsername = User.query.filter_by(username = username).first()
                userEmail = User.query.filter_by(email = email).first()
                if userEmail:
                    flash('Email is already registered', category='error')
                elif userUsername:
                    flash('Username is already taken', category='error')

            if len(email) < 4 or edit.ValidateEmail(email) is False:
                flash('Email is not valid', category='error')
            elif len(firstName) < 1:
                flash('You need to enter your first name', category='error')
            elif len(surname) < 1:
                flash('You need to enter your surname', category='error')
            elif len(username) < 1:
                flash('You need to enter a username', category='error')
            elif len(password) < 1:
                flash('You need to enter a password', category='error')        
            elif len(password) < 8 or edit.ValidatePassword(password) is False:
                flash(
                    'Password needs to be atleast 8 or more characters. Consist of letters (a-z) contain atleast one number (0-9) and special character (@#$%^&+=)', category='error')                
            elif len(repeatPassword) < 1:
                flash('You need to enter both passwords', category='error')
            elif password != repeatPassword:
                flash('Passwords do not match', category='error')
            else:
                flash('User registered', category='success')
                newAccount = User(email = email, firstName = firstName.capitalize(), surname = surname.capitalize(), username = username, password = genHash(password, method='pbkdf2:sha256'))
                Db.session.add(newAccount)
                Db.session.commit()
                flash('User registered', category='success')
                return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
   
@auth.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.search'))
    
    return render_template('result.html', values=dataTuple)

""" Forgot password step 1/3. Enter email adress to get
    a verification code via email."""
@auth.route('/forgotPassowrd', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.login'))
        elif request.form.get('sendCode') == 'sendCode':
            email = request.form.get('email')
            emailRegistered = User.query.filter_by(email = email).first()

            if len(email) < 1:
                flash('You need to enter an email!', category='error')
            elif len(email) < 4 or edit.ValidateEmail(email) is False:
                flash('Email is not valid', category='error')
            else:
                if emailRegistered:
                    flash(' A reset code has been sent to: ' + email, category='success')
                    global token
                    token = generate.GetToken()
                    resetCode = token[1]
                    msg = "You have requested a password reset on your BirdBot account. Here is your reset code: " + resetCode + "\n If this was not you, you can ignore this message. The reset code will be invalid withing 5 minutes."
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(EmailAdress, EmailPassword)
                    server.sendmail(EmailAdress, email, resetCode)

                    return redirect(url_for('auth.enterCode', email = email))

                else:
                    if emailRegistered is None:
                        flash('This email adress is not registered!', category='error')

    return render_template('forgotPassword.html')

""" Forgot password step 2/3. Enter valid reset code from email"""
@auth.route('/enterCode/<email>', methods=['GET', 'POST'])
def enterCode(email):
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.login'))
        else:
            userInput = request.form.get('code')
            global token
            try:
                s = token[2]
                decode = s.loads(token[0])
                code = None
                for key in decode:
                    code = key
            except:
                code = None

            if userInput == code:
                flash('Reset code is valid!', category='success')
                time.sleep(1.5)

                return redirect(url_for('auth.resetPassword', email = email))
            else:
                flash('Reset code is invalid', category='error')

    return render_template('enterCode.html')

                
""" Forgot password step 3/3. Enter new password for account"""
@auth.route('/resetPassword/<email>', methods=['GET', 'POST'])
def resetPassword(email):
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.login'))
        elif request.form.get('reset') == 'reset':
            password = request.form.get('password')
            repeatPassword = request.form.get('repeatPassword')
            
            if len(password) < 1:
                flash('You need to enter a password', category='error')        
            elif len(password) < 8 or edit.ValidatePassword(password) is False:
                flash(
                    'Password needs to be atleast 8 or more characters. Consist of letters (a-z) contain atleast one number (0-9) and special character (@#$%^&+=)', category='error')                
            elif len(repeatPassword) < 1:
                flash('You need to enter both passwords', category='error')
            elif password != repeatPassword:
                flash('Passwords do not match', category='error')
            else:
                user = User.query.filter_by(email = email).first()
                user.password = genHash(password, method='pbkdf2:sha256')
                Db.session.commit()

                flash('Your password has been reset!', category='success')
                time.sleep(1.5)

                return redirect(url_for('auth.login'))
            
    return render_template('resetPassword.html')
