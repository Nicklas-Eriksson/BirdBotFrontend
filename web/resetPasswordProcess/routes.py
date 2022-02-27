from flask import Blueprint, render_template, request, flash, redirect, url_for
import time
from web.resetPasswordProcess.utility import Generate
from web.utility import Edit
import os
from web import Db
from web.models import User
import smtplib
from werkzeug.security import generate_password_hash as genHash
from web.signInProcess.routes import signInBlueprint
from dotenv import load_dotenv

load_dotenv()
EmailAdress = os.getenv("EmailAdress")
EmailPassword = os.getenv("EmailPassword")
resetBlueprint = Blueprint('resetBlueprint', __name__)

""" Forgot password step 1/3. Enter email adress to get
    a verification code via email."""
@resetBlueprint.route('/forgotPassowrd', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.login'))
        elif request.form.get('sendCode') == 'sendCode':
            email = request.form.get('email')
            emailRegistered = User.query.filter_by(email = email).first()

            if len(email) < 1:
                flash('You need to enter an email!', category='error')
            elif len(email) < 4 or Edit.ValidateEmail(email) is False:
                flash('Email is not valid', category='error')
            else:
                if emailRegistered:
                    flash(' A reset code has been sent to: ' + email, category='success')
                    global token
                    token = Generate.GetToken()
                    resetCode = token[1]
                    msg = "You have requested a password reset on your BirdBot account. Here is your reset code: " + resetCode + "\n If this was not you, you can ignore this message. The reset code will be invalid withing 5 minutes."
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(EmailAdress, EmailPassword)
                    server.sendmail(EmailAdress, email, resetCode)

                    return redirect(url_for('resetBlueprint.enterCode', email = email))

                else:
                    if emailRegistered is None:
                        flash('This email adress is not registered!', category='error')

    return render_template('forgotPassword.html')

""" Forgot password step 2/3. Enter valid reset code from email"""
@resetBlueprint.route('/enterCode/<email>', methods=['GET', 'POST'])
def enterCode(email):
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('signIn.login'))
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

                return redirect(url_for('resetBlueprint.resetPassword', email = email))
            else:
                flash('Reset code is invalid', category='error')

    return render_template('enterCode.html')

                
""" Forgot password step 3/3. Enter new password for account"""
@resetBlueprint.route('/resetPassword/<email>', methods=['GET', 'POST'])
def resetPassword(email):
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('auth.login'))
        elif request.form.get('reset') == 'reset':
            password = request.form.get('password')
            repeatPassword = request.form.get('repeatPassword')
            
            if len(password) < 1:
                flash('You need to enter a password', category='error')        
            elif len(password) < 8 or Edit.ValidatePassword(password) is False:
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

                return redirect(url_for('signInBlueprint.login'))
            
    return render_template('resetPassword.html')