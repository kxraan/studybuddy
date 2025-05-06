from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app import bcrypt
from app.models import User
from app.users.forms import (
    RegistrationForm, LoginForm,
    UpdateUsernameForm, UpdateProfilePicForm
)

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
        except Exception:
            flash('Registration failed. Try a different username/email.', 'danger')
    return render_template('users/register.html', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('users.account'))
        flash('Login failed. Check credentials.', 'danger')
    return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('users.login'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    uform = UpdateUsernameForm()
    pform = UpdateProfilePicForm()
    image = current_user.get_profile_pic()

    if uform.submit_username.data and uform.validate_on_submit():
        try:
            current_user.modify(username=uform.username.data.lower())
            current_user.save()
            flash('Username updated!', 'success')
            return redirect(url_for('users.account'))
        except Exception:
            flash('Update failed.', 'danger')

    if pform.submit_picture.data and pform.validate_on_submit():
        pic = pform.picture.data
        if pic:
            data = pic.read()
            if current_user.profile_pic:
                current_user.profile_pic.replace(data, content_type=pic.content_type)
            else:
                current_user.profile_pic.put(data, content_type=pic.content_type)
            current_user.save()
            flash('Profile picture updated!', 'success')
            return redirect(url_for('users.account'))

    return render_template('users/account.html',
                           update_username_form=uform,
                           update_profile_pic_form=pform,
                           image=image)