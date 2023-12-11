# Flask is the class used to create Flas web apps
from flask import Flask
# Extension that helps working with SQL
from flask_sqlalchemy import SQLAlchemy
# Extension for database migrations ASK MIGUEL
from flask_migrate import Migrate
from flask_login import LoginManager


# Configure application
app = Flask(__name__) 
app.secret_key = 'Delfina'

# Name argument determines the root path of the app
# Load the config settings from the config module
app.config.from_object('config') 

# Configure Flas sqlalchemy to use SQLite database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up login manager
login_manager = LoginManager(app)

# We tell Flask-Login where to redirect users when they need to log in
login_manager.login_view = 'login'

# Import the routes and models making them available to the application
from app import models
from app.routes import routes_event, routes_index, routes_log
