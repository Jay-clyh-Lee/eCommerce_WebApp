from flask import render_template, request, session, redirect, flash
from models import user, painting
from __init__ import app
from config.mysqlconnection import connectToMySQL

db = "paintings"

@app.route('/paintings/create', methods=['POST'])
def create():
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "price": request.form["price"],
        "quantity": request.form["quantity"],
        "user_id": session['user_id']
    }
    if not painting.Painting.validate_painting(data):
        return redirect('/paintings/new')
    painting.Painting.create_painting(data)
    return redirect('/dashboard')

@app.route('/paintings/new')
def new():
    user_data = {
        "id": session["user_id"]
    }
    return render_template("new.html", logged_in_user = user.User.get_by_id(user_data))

@app.route('/paintings/show/<int:painting_id>')
def show(painting_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": painting_id,
    }
    return render_template("show.html", logged_in_user = user.User.get_by_id(user_data), painting = painting.Painting.get_by_id(data))

@app.route('/paintings/edit/<int:painting_id>')
def edit(painting_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": painting_id,
    }
    return render_template("edit.html", logged_in_user = user.User.get_by_id(user_data), painting = painting.Painting.get_by_id(data))

@app.route('/paintings/update/<int:painting_id>', methods=['POST'])
def update(painting_id):
    data = {
        "id": painting_id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "price": request.form["price"],
        "quantity": request.form["quantity"],
        "user_id": session['user_id']
    }
    if not painting.Painting.validate_painting(data):
        return redirect(f'/paintings/edit/{painting_id}')
    painting.Painting.update_painting(data)
    return redirect('/dashboard')

@app.route('/paintings/delete/<int:painting_id>')
def destroy(painting_id):
    data = {                                                           
        "id": painting_id
    }
    painting.Painting.destroy_painting(data)
    return redirect('/dashboard')

@app.route('/paintings/<int:painting_id>/buy', methods=['POST'])
def buy_painting(painting_id):
    buyer_data = {  
        "user_id": session['user_id'],
        "painting_id": painting_id
    }
    query = f"UPDATE paintings SET quantity=quantity-1, sold=sold+1 WHERE id = {painting_id};"
    connectToMySQL(db).query_db(query)
    painting.Painting.buy_painting(buyer_data)
    return redirect(f'/paintings/show/{painting_id}')