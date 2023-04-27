"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from models import connect_db, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# TODO: order by with sqlalchemy

@app.get('/')
def homepage():
    """Display Home Page"""

    return redirect("/users")

@app.get("/users")
def users_page():
    """Display user page"""

    users = User.query.order_by(User.first_name).all()

    return render_template("users.html", users = users)

@app.get("/users/new")
def new_user():
    """Display form for a new user"""

    return render_template("new-user.html")

@app.post("/users/new")
def create_new_user():
    """Puts new user into database then redirects to users page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['img_url'] or None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:id>")
def user_profile(id):
    """Display single user profile via user id"""

    user = User.query.get_or_404(id)

    return  render_template("user-profile.html", user = user)


@app.get("/users/<int:id>/edit")
def edit_user_profile(id):
    """Display edit form for user profile"""

    user = User.query.get_or_404(id)

    return  render_template("edit-user.html", user = user)


@app.post("/users/<int:id>/edit")
def save_user_edits(id):
    """Save edits on user profile and redirect to users page"""

    user = User.query.get_or_404(id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return  redirect("/users")

@app.post("/users/<int:id>/delete")
def delete_user(id):
    """Delete a user profile then redirect back to users page"""

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")