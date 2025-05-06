from flask import Flask, render_template, url_for
from mongoengine import connect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

# extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # connect to your MongoDB
    connect(host=app.config['MONGO_URI'])

    # init extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from app.users.routes import users
    app.register_blueprint(users)

    # root route: redirect to login or show home
    @app.route('/')
    def index():
        # Landing page: ask user to login or register
        return render_template('index.html')

    return app