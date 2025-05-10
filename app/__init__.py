from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from .config import Config
import os

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
mongo = PyMongo()  # Global MongoDB client

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Loads config from config.py

    # Initialize extensions
    try:
        mongo.init_app(app)
        app.logger.info("Connected to MongoDB successfully")
    except Exception as e:
        app.logger.error(f"MongoDB connection error: {e}")
        
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.users.routes import users
    app.register_blueprint(users)

    from app.study import study
    app.register_blueprint(study)

    # Landing page route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app