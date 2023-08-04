from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app instance
app = Flask(__name__)

# Configure the database URI (replace 'database_uri' with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'database_uri'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import views and models to register them with the app and database
from . import views
from . import models

app = Flask(__name__)