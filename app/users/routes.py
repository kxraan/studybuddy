from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import bcrypt, mongo
from app.models import User
from app.users.forms import (
    RegistrationForm, LoginForm,
    UpdateUsernameForm, UpdateProfilePicForm
)

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = mongo.db.users.find_one({"username": form.username.data.lower()})
        existing_email = mongo.db.users.find_one({"email": form.email.data.lower()})
        
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('users/register.html', form=form)
        
        if existing_email:
            flash('Email already in use. Please use a different one.', 'danger')
            return render_template('users/register.html', form=form)
        
        # Hash the password    
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create the user document
        user_data = {
            "username": form.username.data.lower(),
            "email": form.email.data.lower(),
            "password": hashed,
            "created_at": datetime.utcnow(),
            "profile_pic": None
        }
        
        try:
            # Insert the user into the database
            mongo.db.users.insert_one(user_data)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('users.login'))
        except Exception as e:
            current_app.logger.error(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('users/register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
        
    form = LoginForm()
    if form.validate_on_submit():
        # Find user by username in MongoDB
        user_data = mongo.db.users.find_one({"username": form.username.data.lower()})
        
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            # Create User object from user_data and login
            user = User(user_data)
            login_user(user, remember=True)  # Enable "remember me" functionality
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('users.account'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))  # Redirect to home page after logout

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    uform = UpdateUsernameForm()
    pform = UpdateProfilePicForm()
    image = current_user.get_profile_pic()
    
    # Handle username form submission
    if uform.submit_username.data and uform.validate_on_submit():
        # Check if new username already exists (and it's not current user's)
        existing = mongo.db.users.find_one({"username": uform.username.data.lower()})
        if existing and existing['_id'] != current_user._id:
            flash('Username already taken.', 'danger')
        else:
            try:
                # Update username in database
                mongo.db.users.update_one(
                    {"username": current_user.username},
                    {"$set": {"username": uform.username.data.lower()}}
                )
                
                # Log the user out to refresh the session (username is used as ID)
                logout_user()
                flash('Username updated successfully! Please log in again.', 'success')
                return redirect(url_for('users.login'))
            except Exception as e:
                current_app.logger.error(f"Username update error: {e}")
                flash('Username update failed.', 'danger')
    
    # Handle profile picture form submission
    if pform.submit_picture.data and pform.validate_on_submit():
        pic = pform.picture.data
        if pic:
            try:
                # Save the image directly to MongoDB using the User model method
                if current_user.save_profile_pic(pic):
                    flash('Profile picture updated successfully!', 'success')
                    return redirect(url_for('users.account'))
                else:
                    flash('Profile picture update failed.', 'danger')
            except Exception as e:
                current_app.logger.error(f"Profile pic update error: {e}")
                flash('Profile picture update failed.', 'danger')
    
    return render_template(
        'users/account.html',
        update_username_form=uform,
        update_profile_pic_form=pform,
        image=image
    )