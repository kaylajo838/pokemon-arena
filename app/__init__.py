from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# registering packages
login = LoginManager(app)

# data manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# configure login settings
login.login_view = 'login'
login.login_message = 'You must be logged in to see this page.'
login.login_message_category = 'warning'

from app import routes, models