from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(1,40)])
    submit_username = SubmitField('Update Username')

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit_picture = SubmitField('Update Picture')