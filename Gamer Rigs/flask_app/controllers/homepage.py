from flask import render_template, redirect, session
from flask_app import app

# track ip address
# track number of visits

@app.route('/')
def index():
    # every time a different visit this webiste, visit ++
    # every time a same ip visit after 24 hours(or less), visit ++
    # ip = '192.168...'
    # visits = 0
    return render_template("home.html")

@app.route('/login_page')
def login_page():
    return render_template("login.html")

@app.route('/signup_page')
def signup_page():
    return render_template("signup.html")