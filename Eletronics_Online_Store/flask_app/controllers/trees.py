from flask import render_template, request, session, redirect, flash
from flask_app.models import user, tree
from flask_app import app

@app.route('/trees/create', methods=['POST'])
def create_tree():
    data = {
        "species" : request.form['species'],
        "locations" : request.form['locations'],
        "reasons" : request.form['reasons'],
        "date_planted": request.form["date_planted"],
        "user_id": session['user_id']
    }
    if not tree.Tree.validate_tree(data):
        return redirect('/trees/new')
    tree.Tree.create_tree(data)
    return redirect('/user/account')

@app.route('/trees/new')
def new_tree():
    user_data = {
        "id": session["user_id"]
    }
    return render_template("new.html", logged_in_user = user.User.get_by_id(user_data))

@app.route('/trees/<int:tree_id>/show')
def show_tree(tree_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": tree_id,
    }
    visit_data = {
        "user_id": session["user_id"],
        "tree_id": session["tree_id"]
    }

    return render_template("show.html", logged_in_user = user.User.get_by_id(user_data), tree = tree.Tree.get_all_by_id(data))
    # return redirect('/trees/{tree_id}/edit)

@app.route('/trees/<int:tree_id>/edit')
def edit_tree(tree_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": tree_id,
    }
    return render_template("edit.html", logged_in_user = user.User.get_by_id(user_data), tree = tree.Tree.get_all_by_id(data))
    # return redirect('/trees/{tree_id}/edit)

@app.route('/trees/<int:tree_id>/update', methods=['POST'])
def update_tree(tree_id):
    data = {
        "id": tree_id,
        "species" : request.form['species'],
        "locations" : request.form['locations'],
        "reasons" : request.form['reasons'],
        "date_planted": request.form["date_planted"],
        # "user_id": session['user_id']
    }
    if not tree.Tree.validate_tree(data):
        return redirect('dashboard')
    tree.Tree.update_tree(data)
    return redirect('/dashboard')
    # return redirect('/trees/{tree_id}/edit)

@app.route('/trees/<int:tree_id>/delete')
def destroy_tree(tree_id):
    data = {                                                           
        # "user_id": session['user_id'],
        "id": tree_id
    }
    tree.Tree.destroy_tree(data)
    return redirect('/dashboard')

@app.route('/trees/<int:tree_id>/visit', methods=['POST'])
def visit_tree(tree_id):
    visitor_data = {  
        "user_id": session['user_id'],
        "tree_id": tree_id
    }
    tree.Tree.visit_tree(visitor_data)
    return redirect('/trees/{tree.id}/show')

@app.route('/trees/<int:tree_id>/dislike', methods=['POST'])
def dislike_tree(tree_id):
    liker_data = {  
        "user_id": session['user_id'],
        "tree_id": tree_id
    }
    tree.Tree.dislike_tree(liker_data)
    return redirect('/dashboard')