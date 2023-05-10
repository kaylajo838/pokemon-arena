from flask import render_template, request, flash, redirect, url_for
from app.blueprints.auth import auth
from .forms import RegistrationForm, LoginForm, EditProfileForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_dict = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        # create instance of User
        new_user = User()
        # implementing values from our form data for our instance
        new_user.from_dict(new_user_dict)

        new_user.save_to_db()

        flash('Nice! You are officially registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('registration.html', form=form, active_page='registration')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in! Welcome back, {queried_user.first_name}!', 'success')
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form, active_page='login')


@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have been logged out, see you next time!', 'warning')
        return redirect(url_for('auth.login'))
    
@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_dict = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': current_user.password
        }

        # Query current user from db to change
        queried_user = User.query.filter_by(email=new_user_dict['email']).first()

        # Check if queried_user already exists
        if queried_user:
            flash('Email is already in use.', 'danger')
            return redirect(url_for('edit_profile'))
        else:
            # Add changes to db
            current_user.update_from_dict(new_user_dict)
            current_user.save_to_db()
            flash('Profile Updated!', 'success')
            return redirect(url_for('main.home'))
        
    return render_template('edit_profile.html', form=form, active_page='edit_profile')