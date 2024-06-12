from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required

from .models.user import User
from .extensions import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    # print(user)
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    login_user(user, remember=remember)
    return redirect(url_for('home'))


@auth.route('/register')
def register():
    return render_template("register.html")


@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists')
        return redirect(url_for('register'))
    if password != password_confirmation:
        flash('Password and password are not the same')
        return redirect(url_for('register'))
    new_user = User(username=username, firstName=firstname, lastName=lastname)
    # print(new_user)
    new_user.set_password(password)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
