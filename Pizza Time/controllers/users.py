from flask import render_template, request, session, redirect, flash
from models import user, order
from __init__ import app
from flask_bcrypt import Bcrypt  

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/signup')

@app.route('/signup')
def signUp():
    return render_template("register.html")

@app.route('/signon')
def signOn():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])                               
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
        "address": request.form['address'],
        "city": request.form['city'],
        "state": request.form['state'],
    }
    session['user_id'] = user.User.create_user(user_data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not user.User.validate_login(request.form):
        return redirect('/')
    user_data = {
        'email':request.form['email']
    } 
    user_with_email = user.User.get_by_email(user_data)
    if not user_with_email:
        flash("incorrect email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        flash("incorrect email/password", "login")
        return redirect('/')
    session['user_id'] = user_with_email.id
    flash("successfully logged in.")
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/account')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session["user_id"]
    }
    return render_template("account.html", logged_in_user = user.User.get_by_id(data), all_orders = order.Order.get_all())
