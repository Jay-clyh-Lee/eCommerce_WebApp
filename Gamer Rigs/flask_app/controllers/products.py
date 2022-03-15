from flask import render_template, request, session, redirect, flash
from flask_app.models import user, admin, product
from flask_app import app

@app.route('/products')
def show_products():
    all_products = product.Product.get_all()
    return render_template("products.html", all_products = all_products)

@app.route('/<int:category_id>/products')
def show_products_by_category(category_id):
    return render_template("products.html", products = product.Product.get_all_by_category(category_id))

@app.route('/product/<int:product_id>')
def view_a_product(product_id):
    return render_template("product.html", product = product.Product.get_by_id(product_id))


@app.route('/product/<int:product_id>/order', methods=['POST'])
def create_order(product_id):
    if "user_id" not in session:
        return redirect('login.html')
    order_data = {
        "id": session["user_id"],
        "product_id": product_id,
        "shipping_address": request.form["shipping_address"],
    }
    product.Product.create_order(order_data)
    return redirect('/dashboard')