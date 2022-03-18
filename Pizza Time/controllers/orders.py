from flask import render_template, request, session, redirect, flash
from models import user, order, product
from __init__ import app
from config.mysqlconnection import connectToMySQL

db = "pizza_time"

@app.route('/orders/cart')
def carting():



@app.route('/orders/create', methods=['POST'])
def create():
    product_data = {
        "method" : request.form['method'],
        "size" : request.form['size'],
        "crust": request.form["crust"],
        "toppings": request.form["toppings"],
        "favorite": request.form["favorite"],
    }
    if not product.Product.validate_product(product_data):
        return redirect('/orders/new')

    final_price = order.Order.single_item_price(product_data["method"], product_data["size"], product_data["crust"], product_data["toppings"])
    final_price = order.Order.calculate_final_price(request.form['quantity'], 7.5) #7.5 is tax%
    
    order_data = {
        "quantity": request.form["quantity"],
        "price": final_price,
        "user_id": session['user_id'],
        "product_id": session['product_id']
    }
    
    if not order.Order.validate_order(order_data):
        return redirect('/orders/new')

    product.Product.create_product(product_data)
    order.Order.create_order(order_data)
    return redirect('/dashboard')

@app.route('/orders/new')
def new():
    user_data = {
        "id": session["user_id"]
    }
    return render_template("new.html", logged_in_user = user.User.get_by_id(user_data))

@app.route('/orders/show/<int:order_id>')
def show(order_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": order_id,
    }
    return render_template("show.html", logged_in_user = user.User.get_by_id(user_data), order = order.order.get_by_id(data))

@app.route('/orders/edit/<int:order_id>')
def edit(order_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": order_id,
    }
    return render_template("edit.html", logged_in_user = user.User.get_by_id(user_data), order = order.order.get_by_id(data))

@app.route('/orders/update/<int:order_id>', methods=['POST'])
def update(order_id):
    data = {
        "method" : request.form['method'],
        "size" : request.form['size'],
        "crust": request.form["crust"],
        "toppings": request.form["toppings"],
        "quantity": request.form["quantity"],
        "favorite": request.form["favorite"],
        "user_id": session['user_id']
    }
    if not order.order.validate_order(data):
        return redirect(f'/orders/edit/{order_id}')
    order.order.update_order(data)
    return redirect('/dashboard')

@app.route('/orders/delete/<int:order_id>')
def destroy(order_id):
    data = {                                                           
        "id": order_id
    }
    order.order.destroy_order(data)
    return redirect('/dashboard')

@app.route('/orders/<int:order_id>/buy', methods=['POST'])
def buy_order(order_id):
    buyer_data = {  
        "user_id": session['user_id'],
        "order_id": order_id
    }
    query = f"UPDATE orders SET quantity=quantity-1, sold=sold+1 WHERE id = {order_id};"
    connectToMySQL(db).query_db(query)
    order.order.buy_order(buyer_data)
    return redirect(f'/orders/show/{order_id}')