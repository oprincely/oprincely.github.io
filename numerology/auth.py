from flask import Blueprint, render_template, redirect, url_for,session, request, flash
import re
#from sqlalchemy import *

import datetime
x = datetime.datetime.now()
year_now = x.year

import mysql.connector
from mysql.connector import Error

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
    
    try:
        connection = mysql.connector.connect(host='localhost',database='wecorgng_user',user='wecorgng',password='spyWIZARD')
        
        cursor = connection.cursor(prepared=True)
        
        
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
    
        #print("Laptop price is : ", user)
        
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
    
    except mysql.connector.Error as error:
        print("Failed to get record from database: {}".format(error))
        
    # If account exists in accounts table in out database
    if user:
        # Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['id'] = user[0]
        session['username'] = user[3]
        # Redirect to home page
        return redirect(url_for('main.profile'))
        #return 'Logged in successfully!'
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
    
        
    return render_template('auth/login.html', msg=msg,year_now=year_now)
    


@auth.route('/signup')
def signup():
    return render_template('auth/register.html',year_now=year_now)

@auth.route('/signup', methods=['POST'])
def signup_post():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        fname = request.form['firstname']
        mname = request.form['middlename']
        surname = request.form['surname']
        dob = request.form['dob']
        tob = request.form['tob']
        pob = request.form['placeofbirth']
        mobile = request.form['phone']
        
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        number_of_quesion = 0
        
        user_question = ''
        admin_ans = ''
        
        # Check if account exists using MySQL
        try:
            connection = mysql.connector.connect(host='localhost',database='wecorgng_user',user='wecorgng',password='spyWIZARD')
            
            cursor = connection.cursor(prepared=True)
            
            
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
        
            
        
            # If account exists show error and validation checks
            if user:
                msg = 'Account already exists!'
                return render_template('auth/login.html', msg=msg,year_now=year_now)
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (fname,mname,surname,dob,tob,pob,mobile,email, password, username, number_of_quesion,user_question,admin_ans))
                
                connection.commit()
                
                msg = 'You have successfully registered!'
                
                #print("successfully added a user : ", username)
                
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
                    #print("MySQL connection is closed")
        
        except mysql.connector.Error as error:
            print("Failed to get record from database: {}".format(error))
            
        msg = 'You have successfully registered!'
        return render_template('auth/login.html', msg=msg,year_now=year_now)
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('auth/register.html', msg=msg,year_now=year_now)

@auth.route('/logout')
#@login_required
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    # Redirect to login page
    return redirect(url_for('main.index'))