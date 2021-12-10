from flask import render_template, request, session, redirect, flash
from flask_app.models import user, admin, product
from flask_app import app

@app.route('/products')
def show_products():
    all_products = product.Product.get_all()
    return render_template("products.html", all_products = all_products)

@app.route('/<int:category_id>/<int:product_id>/order')
def create_order(category_id, product_id):
    if "user_id" not in session:
        return redirect('home.html')
    order_data = {
        "id": session["user_id"],
        "category_id": category_id,
        "product_id": product_id 
    }
    product.Product.create_order(order_data)
    return redirect('product.html')

@app.route('/<int:category_id>/show')
def show_category():
    return render_template('category.html')

@app.route('/<int:category_id>/<int:product_id>/show')
def show_product():
    return render_template('product.html')

