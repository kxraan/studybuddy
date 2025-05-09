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

# Create mongo global variable to use across app
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize PyMongo with the app
    try:
        mongo.init_app(app)
        app.logger.info("Connected to MongoDB successfully")
    except Exception as e:
        app.logger.error(f"MongoDB connection error: {e}")
    
    # Init extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Register blueprint
    from app.users.routes import users
    app.register_blueprint(users)

    from app.study import study
    app.register_blueprint(study)

    
    # Landing page prompts login or register
    @app.route('/')
    def index():
        return render_template('index.html')
        
    return app