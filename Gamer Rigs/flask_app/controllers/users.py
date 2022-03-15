from flask import render_template, request, session, redirect, flash
from flask_app.models import user, tree
from flask_app import app
from flask_bcrypt import Bcrypt  

from 

bcrypt = Bcrypt(app)

# @app.route('/')
# def index():
#     return render_template("home.html")

@app.route('/register',methods=['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])                               
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
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

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", logged_in_user = user.User.get_by_id(data), user_products = product.Product.get_all_by_user(data))

@app.route('/update', methods=['POST'])
def update():
    if "user_id" not in session:
        return redirect('/')
    
    data = {
        "title": request.form['title']       
    }
    user.User.update_user(request.form)
    return redirect('/dashboard')

@app.route('/user/account')
def account():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session["user_id"]
    }
    return render_template("account.html", logged_in_user = user.User.get_by_id(data), all_trees = tree.Tree.get_my_trees(data))
