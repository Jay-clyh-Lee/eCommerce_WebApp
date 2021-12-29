from flask import render_template, request, session, redirect, flash
from flask_app.models import user, admin, product
from flask_app import app

@app.route('/<string:category>')
def show_category(category):
    return render_template("products.html", category = category, roducts = product.Product.get_all_by_category(category))



@app.route('/<string:category>/products')
def show_products():
    all_products = product.Product.get_all()
    return render_template("products.html", all_products = all_products)

@app.route('/<string:category>/<int:category_id>/<int:product_id>/order', methods=['POST'])
def create_order(category_id, product_id):
    if "user_id" not in session:
        return redirect('login.html')
    order_data = {
        "id": session["user_id"],
        "category_id": category_id,
        "product_id": product_id,
        "shipping_address": request.form["shipping_address"],
    }
    product.Product.create_order(order_data)
    return redirect('product.html')

@app.route('/<int:category_id>/show')
def show_category():
    return render_template('category.html')

@app.route('/<int:category_id>/<int:product_id>/show')
def show_product():
    return render_template('product.html')

