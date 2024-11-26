from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# Configurations (you can move this to config.py later)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:201830011@localhost/urm_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize extensions
db = SQLAlchemy(app)
# db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


# Register blueprints (routes)
from app.routes.shared import shared
from app.routes.api import api


app.register_blueprint(shared, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")

