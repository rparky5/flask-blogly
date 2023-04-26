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

@app.get('/')
def show_homepage():
    """Display Home Page"""

    return render_template("base.html")



@app.post("/")
def process_incoming_data():
    """Process the post requests on homepage"""


@app.get("/user")
def show_users_page():
    """Display user page"""

    users = User.query.all()
    return render_template("user.html", users = users)

@app.get("/user/<int:id>")
def show_user_profile(id):
    """Display single user profile via user id"""

    return  render_template("user_profile.html")