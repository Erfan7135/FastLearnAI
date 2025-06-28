import uuid
from app.web.app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model for storing user information."""
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the user's password."""
        return check_password_hash(self.password_hash, password)
    


class Pdf(db.Model):
    """Model for storing PDF documents."""
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref=db.backref('pdfs', lazy=True))