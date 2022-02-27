from flask import session, Blueprint, render_template, request, flash, redirect, url_for, Flask, make_response
from flask_login import login_required, login_user, logout_user, current_user
from web.searchProcess.routes import search
from web.utility import Edit
import time
from web.models import User
from web import Db
from werkzeug.security import generate_password_hash as genHash, check_password_hash as checkHash


signInBlueprint = Blueprint('signInBlueprint', __name__)

@signInBlueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('signInBlueprint.login'))

        else:
            email = request.form.get('email')
            firstName = request.form.get('firstName')
            surname = request.form.get('surname')
            username = request.form.get('username')
            password = request.form.get('password')
            repeatPassword = request.form.get('repeatPassword')

            if email and firstName and surname and username and password and repeatPassword:
                credentials = Edit.RemoveWhitespaceRegister(email, firstName, surname, username, password, repeatPassword)
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

            if len(email) < 4 or Edit.ValidateEmail(email) is False:
                flash('Email is not valid', category='error')
            elif len(firstName) < 1:
                flash('You need to enter your first name', category='error')
            elif len(surname) < 1:
                flash('You need to enter your surname', category='error')
            elif len(username) < 1:
                flash('You need to enter a username', category='error')
            elif len(password) < 1:
                flash('You need to enter a password', category='error')        
            elif len(password) < 8 or Edit.ValidatePassword(password) is False:
                flash(
                    'Password needs to be atleast 8 or more characters. Consist of letters (a-z), contain atleast one number (0-9) and special character (@#$%^&+=)', category='error')                
            elif len(repeatPassword) < 1:
                flash('You need to enter both passwords', category='error')
            elif password != repeatPassword:
                flash('Passwords do not match', category='error')
            else:
                newAccount = User(email = email, firstName = firstName.capitalize(), surname = surname.capitalize(), username = username, password = genHash(password, method='pbkdf2:sha256'))
                Db.session.add(newAccount)
                Db.session.commit()
                flash('User registered', category='success')
                return redirect(url_for('signInBlueprint.login'))

    return render_template('register.html')

@signInBlueprint.route('/', methods=['GET', 'POST'])
@signInBlueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('signInBlueprint.register'))
        elif request.form.get('forgotPass') == 'forgotPass':
            return redirect(url_for('resetBlueprint.forgotPassword'))
        else:
            username = request.form.get('username')
            password = request.form.get('password')   

            if len(username) < 1:
                flash('You need to enter a username', category='error')
            elif len(password) < 1:
                flash('You need to enter a password', category='error')

            if username and password:
                credentials = Edit.RemoveWhitespaceLogin(username, password)
                username = credentials[0]
                password = credentials[1]

                user = User.query.filter_by(username = username).first()
            
                if user:
                    if checkHash(user.password, password):
                        
                        login_user(user, remember=True)
                        flash('Welcome!', category='success')
                        time.sleep(1.5)

                        return redirect(url_for('searchBlueprint.search', username = username))
                    else:
                        flash('Incorrect credentials', category='error')
                else:
                    flash('Incorrect credentials', category='error')
        
    return render_template('login.html')

@signInBlueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signInBlueprint.login'))