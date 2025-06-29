import os
from flask import Flask, session, g
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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    # If you are using SQLite, you can change the URI to 'sqlite:///app.db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 

    if not app.config['SECRET_KEY']:
        raise ValueError("No SECRET_KEY set for Flask application. Please set the SECRET_KEY environment variable.")
    
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['TEMP_FOLDER'] = os.getenv('TEMP_FOLDER', 'temp')
    
    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints
    from app.web.views.auth_views import auth_bp
    from app.web.views.pdf_views import pdf_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(pdf_bp)

    @app.before_request
    def load_logged_in_user():
        """Load the logged-in user into the global context."""
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            from app.web.db.models.base import User
            g.user = User.find_by(id=user_id)


    # A simple route for testing
    @app.route('/')
    def home():
        return "Welcome to the Fast Learn App!"
    
    # Register blueprints or other components here
    
    return app
