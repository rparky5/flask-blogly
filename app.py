"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from models import connect_db, User, db, Post

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
    image_url = request.form['image_url'] or None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def user_profile(user_id):
    """Display single user profile via user id"""

    user = User.query.get_or_404(user_id)

    return  render_template("user-profile.html", user = user)


@app.get("/users/<int:user_id>/edit")
def edit_user_profile(user_id):
    """Display edit form for user profile"""

    user = User.query.get_or_404(user_id)

    return  render_template("edit-user.html", user = user)


@app.post("/users/<int:user_id>/edit")
def save_user_edits(user_id):
    """Save edits on user profile and redirect to users page"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()

    return  redirect("/users")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a user profile then redirect back to users page"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Display form to make a new post"""

    user = User.query.get_or_404(user_id)

    return render_template("new-post.html", user=user)

@app.post("/users/<int:user_id>/posts/new")
def create_new_post(user_id):
    """Create new post and redirect to user profile page"""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title = title, content = content, user_id = user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def view_post(post_id):
    """View a specific post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)