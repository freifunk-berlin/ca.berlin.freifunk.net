from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)
db = SQLAlchemy(app)
mail = Mail(app)

# Load the default configuration
app.config.from_object('config')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

import ca.views
