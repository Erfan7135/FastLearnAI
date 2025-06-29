import uuid
from app.web.app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class BaseModel(db.Model):
    __abstract__ = True  # This tells SQLAlchemy that this is an abstract model and should not be created as a table.

    @classmethod
    def find_by(cls, **kwargs):
        """Find a element by given attributes."""
        return cls.query.filter_by(**kwargs).first()
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new element with the given attributes."""
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

class User(BaseModel):
    """User model for storing user information."""

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    pdfs = relationship('Pdf', back_populates='user', lazy=True)

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def as_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }
    


class Pdf(BaseModel):
    """Model for storing PDF documents."""
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    user = relationship('User', back_populates='pdfs')

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "file_path": self.file_path
        }