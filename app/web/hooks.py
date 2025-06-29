import os
import uuid
from functools import wraps
from flask import request, jsonify, Blueprint, g, session, current_app
from app.web.db.models.base import User

def login_required(view):
    """Decorator to ensure the user is logged in."""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'error': 'Unauthorized'}), 401
        g.user = User.query.filter_by(id=user_id).first()
        if g.user is None:
            return jsonify({'error': 'Unauthorized'}), 401
        return view(*args, **kwargs)
    return wrapped_view

def handle_file_upload(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        print(request.files)
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Invalid file type, only PDF allowed'}), 400

        # Generate a unique filename and path for temporary storage
        file_id = str(uuid.uuid4())
        original_filename = file.filename
        temp_file_path = os.path.join(current_app.config['TEMP_FOLDER'], file_id + '.pdf') # Use a temp directory

        # Create temp directory if it doesn't exist
        if not os.path.exists(current_app.config['TEMP_FOLDER']):
            os.makedirs(current_app.config['TEMP_FOLDER'])

        file.save(temp_file_path)

        # Pass file_id, temp_file_path, and original_filename to the view function
        return view(file_id=file_id, file_path=temp_file_path, file_name=original_filename, *args, **kwargs)
    return wrapped_view