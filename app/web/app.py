import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Set configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints
    from app.web.views.auth_views import auth_bp
    from app.web.views.pdf_views import pdf_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(pdf_bp)


    # A simple route for testing
    @app.route('/')
    def home():
        return "Welcome to the Fast Learn App!"
    
    # Register blueprints or other components here
    
    return app
