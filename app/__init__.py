from flask import Flask, render_template
from mongoengine import connect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config  # Fixed import - Config is in project root, not app folder

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Connect to MongoDB - Fixed to use proper string connection
    try:
        connect(db='studybuddy', host=app.config['MONGO_URI'])
    except Exception as e:
        app.logger.error(f"MongoDB connection error: {e}")
    
    # Init extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprint
    from app.users.routes import users
    app.register_blueprint(users)
    
    # Landing page prompts login or register
    @app.route('/')
    def index():
        return render_template('index.html')
        
    return app