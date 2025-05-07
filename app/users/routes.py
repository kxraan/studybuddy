from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app import bcrypt
from app.models import User
from app.users.forms import (
    RegistrationForm, LoginForm,
    UpdateUsernameForm, UpdateProfilePicForm
)

users = Blueprint('users', __name__, url_prefix='/users')  # Added url_prefix for consistency

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.objects(username=form.username.data.lower()).first()
        existing_email = User.objects(email=form.email.data.lower()).first()
        
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('users/register.html', form=form)
        
        if existing_email:
            flash('Email already in use. Please use a different one.', 'danger')
            return render_template('users/register.html', form=form)
            
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data.lower(),
            email=form.email.data.lower(),
            password=hashed
        )
        
        try:
            user.save()
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
        user = User.objects(username=form.username.data.lower()).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
        existing = User.objects(username=uform.username.data.lower()).first()
        if existing and existing.id != current_user.id:
            flash('Username already taken.', 'danger')
        else:
            try:
                current_user.username = uform.username.data.lower()
                current_user.save()
                flash('Username updated successfully!', 'success')
                return redirect(url_for('users.account'))
            except Exception as e:
                current_app.logger.error(f"Username update error: {e}")
                flash('Username update failed.', 'danger')
    
    # Handle profile picture form submission
    if pform.submit_picture.data and pform.validate_on_submit():
        pic = pform.picture.data
        if pic:
            try:
                data = pic.read()
                if current_user.profile_pic:
                    current_user.profile_pic.replace(data, content_type=pic.content_type)
                else:
                    current_user.profile_pic.put(data, content_type=pic.content_type)
                current_user.save()
                flash('Profile picture updated successfully!', 'success')
                return redirect(url_for('users.account'))
            except Exception as e:
                current_app.logger.error(f"Profile pic update error: {e}")
                flash('Profile picture update failed.', 'danger')
    
    return render_template(
        'users/account.html',
        update_username_form=uform,
        update_profile_pic_form=pform,
        image=image
    )