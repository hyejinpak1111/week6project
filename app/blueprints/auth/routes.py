from . import bp as app
from app.blueprints.main.models import User
from app import db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.blueprints.auth.forms import SignupForm, Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'GET':
            return render_template('login.html', form = form)
    if form.validate_on_submit():        
        try:
            if form.validate_on_submit():
                name = form.name.data
                password = form.password.data
    
                user = User.query.filter_by(name=name).first()

                if user is None:
                    flash('There was not a user with that email.', 'danger')
                elif not user.check_my_password(password):
                    flash('The password was incorrect.', 'danger')
                else:
                    flash('Logged in successfully', 'success')
                    login_user(user)
                    return redirect(url_for('main.home'))
            # flash('User logged in successfully', 'success')
            # return render_template('login.html')
        except:
            raise Exception('Invalid form data.')
    return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('register.html', form = form)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            name = form.name.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            check_user = User.query.filter_by(email=email).first()

            if check_user is not None:
                flash('A user with this email already exists.', 'danger')

            elif password != confirm_password:
                flash('The passwords do not match', 'danger')

            new_user = User(email=email, name=name, password='')
            new_user.hash_my_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully', 'success')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid form data.')

@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out', 'success')
    return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You can't access this page without logging in", "danger")
    return redirect(url_for('auth.login'))