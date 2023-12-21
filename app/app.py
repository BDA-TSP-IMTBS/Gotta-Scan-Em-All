from crypt import methods
from typing import List, Dict
from flask import Flask, render_template, request, make_response, request, jsonify, url_for, session, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
from passlib.hash import sha256_crypt
from werkzeug.exceptions import HTTPException
import secrets
import mysql.connector
import json
import re
import os

app = Flask(__name__)

# Secret key
# DON'T SHOW THIS TO ANYONE
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('DB_DB', 'pythonlogin')
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)

# Initialize items page
with open("./items.json", "r") as f:
  data = json.load(f)
items = data["items"]

# Home Page
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
# Login endpoint
@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            if sha256_crypt.verify(password, account['password']):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['score'] = account['score']
                session['inventory'] = account['inventory']
                session['lastScanTime'] = account['lastScanTime']
                # Redirect to home page
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)
  
# Lougout endpoint    
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('score', None)
   session.pop('inventory', None)
   session.pop('lastScanTime', None)
   # Redirect to login page
   return redirect(url_for('login'))

# Register endpoint
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = sha256_crypt.encrypt(request.form['password'])
        base_inventory = "0"*len(items)
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, 0, %s, DEFAULT)', (username, password, base_inventory,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# Profile page
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        img = []
        for i, e in enumerate(account["inventory"]):
            if e=="1":
                img.append(i)
        
        return render_template('profile.html', account=account, items=items, img=img)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Items page
@app.route('/<string:slug>')
def seeItem(slug):
    if 'loggedin' in session:
        slugList = [item["slug"] for item in items]
        if slug in slugList:
            id = slugList.index(slug)
            
            if session["inventory"][id] == "0":
                # First time seeing the card
                hasAlreadySeen = False
                
                # Change inventory and score
                session["inventory"] = session["inventory"][0:id] + "1" + session["inventory"][id+1: ]
                session["score"] = str( int(session["score"]) + items[id]["pointsMin"] )
                
                # Update database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
                account = cursor.fetchone()
                
                if account:
                    cursor.execute('UPDATE accounts SET score = %s, inventory = %s WHERE id = %s', (session["score"], session["inventory"], session["id"],))
                    mysql.connection.commit()
                else:
                    return "You're not logged in are you ?"
                
            else:
                hasAlreadySeen = True
            return render_template('item.html', item=items[id], hasAlreadySeen=hasAlreadySeen)
    
    return redirect(url_for('home'))
    
# Scoreboard page
@app.route('/scoreboard')
def scoreboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username, score FROM accounts ORDER BY score DESC, lastScanTime ASC')
    rows = cursor.fetchall()
    
    return render_template('scoreboard.html', rows=rows)
    


if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0')
